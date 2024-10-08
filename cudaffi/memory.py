from __future__ import annotations

import ctypes
from abc import ABC, abstractmethod
from typing import NewType

from cuda import cudart

from .core import init
from .utils import checkCudaErrors

NvDeviceMemory = NewType("NvDeviceMemory", object)  # cuda.CUdeviceptr
NvHostMemory = NewType("NvHostMemory", object)
NvManagedMemory = NewType("NvManagedMemory", object)


class CudaMemory(ABC):
    def __init__(self, size: int):
        init()

        self.size = size
        self.ctype = ctypes.c_void_p

    # allocates the memory

    # @abstractmethod
    # def set(self, dest_data: Any) -> None: ...

    # copies from memory to the target destination using a datatype converter

    # @abstractmethod
    # def get(self, src_data: Any) -> None: ...

    # copies data from src to this memory location using a datatype converter

    # @abstractmethod
    # def free(self) -> None: ...

    # deallocates the memory

    @property
    @abstractmethod
    def dev_addr(self) -> NvDeviceMemory | NvManagedMemory: ...

    def copy_to(self, dst_mem: CudaMemory) -> None:
        pass

    # copies between memory locations

    def copy_from(self, src_mem: CudaMemory) -> None:
        pass

    # copies between memory locations

    @staticmethod
    def memcpy(src: CudaMemory, dst: CudaMemory) -> None:
        pass


class CudaHostMemory(CudaMemory):
    def __init__(self, size: int) -> None:
        super().__init__(size)

        flags = cudart.cudaHostAllocDefault
        self.nv_host_memory: NvHostMemory = checkCudaErrors(cudart.cudaHostAlloc(size, flags))
        print("self.nv_host_memory", self.nv_host_memory.__class__)

    @property
    def dev_addr(self) -> NvDeviceMemory:
        raise Exception("attempting to use host memory as device address")


class CudaDeviceMemory(CudaMemory):
    def __init__(self, size: int) -> None:
        super().__init__(size)

        self.nv_device_memory: NvDeviceMemory = checkCudaErrors(cudart.cudaMalloc(size))
        print("self.nv_device_memory", self.nv_device_memory.__class__)

    @property
    def dev_addr(self) -> NvDeviceMemory:
        return self.nv_device_memory


class CudaManagedMemory(CudaMemory):
    def __init__(self, size: int) -> None:
        super().__init__(size)

        flags = cudart.cudaMemAttachGlobal
        self.nv_managed_memory: NvManagedMemory = checkCudaErrors(
            cudart.cudaMallocManaged(size, flags)
        )
        print("self.nv_managed_memory", self.nv_managed_memory.__class__)

    @property
    def dev_addr(self) -> NvManagedMemory:
        return self.nv_managed_memory
