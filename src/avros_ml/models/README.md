# models/

Drop trained weights here (YOLO `.engine`, TCN `.pt`) together with a spec file based on
`example_model.yaml`. Weight files are git-ignored because they are large; share them
through git-lfs, a release asset, or a download script instead.

TensorRT engines are tied to the GPU and TensorRT version: build them on the Jetson AGX
Orin itself.
