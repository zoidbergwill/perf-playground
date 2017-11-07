#!/usr/bin/python
from bcc import BPF
import ctypes as ct

b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/blkdev.h>

struct data_t {
    u64 delta;
    u64 ts;
};
BPF_PERF_OUTPUT(events);

BPF_HASH(last);

int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, key = 0;

    // attempt to read stored timestamp
    tsp = last.lookup(&key);
    if (tsp != 0) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            struct data_t data = {};
            data.ts = bpf_ktime_get_ns();
            data.delta = delta;
            events.perf_submit(ctx, &data, sizeof(data));
        }
        last.delete(&key);
    }

    // update stored timestamp
    ts = bpf_ktime_get_ns();
    last.update(&key, &ts);
    return 0;
}
""")

b.attach_kprobe(event="sys_sync", fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

# define output data structure in Python
class Data(ct.Structure):
    _fields_ = [("delta", ct.c_ulonglong),
                ("ts", ct.c_ulonglong)]

# header
print("%-18s %-16s" % ("TIME(s)", "MESSAGE"))

# process event
start = 0
def print_event(cpu, data, size):
    global start
    event = ct.cast(data, ct.POINTER(Data)).contents
    if start == 0:
            start = event.ts
    time_s = (float(event.ts - start)) / 1000000000
    print("%-18.9f multiple syncs detected, last %s ms ago" % (time_s, event.delta / 1000000))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    b.kprobe_poll()
