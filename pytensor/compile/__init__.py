from pytensor.compile.function.pfunc import pfunc, rebuild_collect_shared
from pytensor.compile.function.types import (
    AliasedMemoryError,
    Function,
    FunctionMaker,
    Supervisor,
    UnusedInputError,
    alias_root,
    convert_function_input,
    fgraph_updated_vars,
    get_info_on_inputs,
    infer_reuse_pattern,
    insert_deepcopy,
    orig_function,
    std_fgraph,
    view_tree_set,
)
from pytensor.compile.io import In, Out, SymbolicInput, SymbolicOutput
from pytensor.compile.mode import (
    FAST_COMPILE,
    FAST_RUN,
    JAX,
    NUMBA,
    OPT_FAST_COMPILE,
    OPT_FAST_RUN,
    OPT_FAST_RUN_STABLE,
    OPT_MERGE,
    OPT_NONE,
    OPT_O2,
    OPT_O3,
    OPT_STABILIZE,
    OPT_UNSAFE,
    PYTORCH,
    AddDestroyHandler,
    AddFeatureOptimizer,
    Mode,
    PrintCurrentFunctionGraph,
    get_default_mode,
    get_mode,
    local_useless,
    optdb,
    predefined_linkers,
    predefined_modes,
    predefined_optimizers,
    register_linker,
    register_mode,
    register_optimizer,
)
from pytensor.compile.monitormode import MonitorMode
from pytensor.compile.ops import (
    DeepCopyOp,
    FromFunctionOp,
    ViewOp,
    as_op,
    deep_copy_op,
    register_deep_copy_op_c_code,
    register_view_op_c_code,
    view_op,
)
from pytensor.compile.profiling import ProfileStats
from pytensor.compile.sharedvalue import SharedVariable, shared, shared_constructor
