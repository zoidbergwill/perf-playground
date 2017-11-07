#!/usr/bin/env python
from bcc import BPF

bpf = BPF(text='int kprobe__sys_sync(void *ctx) { bpf_trace_printk("sys_sync() called\\n"); return 0; }')

if __name__ == '__main__':
	print('Tracing sys_sync()... Ctrl-C to end.')
	bpf.trace_print()
