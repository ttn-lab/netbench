# Netbench

Netbench is a CLI utlity for running benchmarks in a network. It allows
measuring bandwidth or synchronization between devices. Mainly, Netbench acts
as a wrapper around other well-established tools, offering a consistent and
convenient interface for runnings all the necessary benchmarks from one place
and also providing results in an analytics-friendly format.

## Pre-requisites for installation

Netbench relies on [iperf3](https://github.com/esnet/iperf) for bandwidth
measurements and injecting load into the network. Some Linux distributions
offer it in a package, but you can always build it from source.

For PTP synchronization benchmarking, the
[linuxptp](https://github.com/richardcochran/linuxptp) tools are used. Again,
packages are available in some distributions.

## Installing netbench

Simply install it with pip:

```shell
pip install --user netbench
```

Note that, to be able to use the `netbench` command, the pip installation
directory must be present in your `PATH`.
