#include <stdint.h>

// TODO: auto generate macros for each individual possible operation and type.
//  this leaves the definition of optionals (etc) and checkedcasting into a
//  lang implementor issue.

#define number_template(typename, nativetype) \
    typedef struct typename { nativetype native; } type_##typename; \
    type_##typename dflt_##typename () { return (type_##typename){0}; } \
    type_##typename get_##typename (type_##typename self) { return self; } \
    void rtn_##typename (type_##typename self) { return; } \
    void rel_##typename (type_##typename self) { return; } \
    type_##typename litrl_##typename (nativetype val) { return (type_##typename){val}; } \

    // cntn expose not required

#define arith_op_template(outtype, opname, atype, nativeop, btype) \
    type_##outtype opname##_##atype##_##btype (type_##atype a, type_##btype b) { \
        return (type_##outtype) { a.native nativeop b.native}; \
    }

#define cast_template(totype, fromtype) \
    type_##totype cast_##fromtype##_to_##totype (type_##fromtype val) { \
        return (type_##totype) { val.native };\
    }

number_template(uint64, uint64_t)
number_template(uint32, uint32_t)
number_template(uint16, uint16_t)
number_template(uint8,  uint8_t)

number_template(int64, int64_t)
number_template(int32, int32_t)
number_template(int16, int16_t)
number_template(int8,  int8_t)

number_template(float32, float)
number_template(float64, double)

cast_template(uint64, uint32) cast_template(int64, int32)
cast_template(uint64, uint16) cast_template(int64, int16)
cast_template(uint64,  uint8) cast_template(int64,  int8)

cast_template(uint32, uint16) cast_template(int32, int16)
cast_template(uint32,  uint8) cast_template(int32,  int8)

cast_template(uint16,  uint8) cast_template(int16,  int8)

cast_template(float64, float32)

// same adds
arith_op_template(uint64, add, uint64, +, uint64) arith_op_template(int64, add, int64, +, int64)
arith_op_template(uint32, add, uint32, +, uint32) arith_op_template(int32, add, int32, +, int32)
arith_op_template(uint16, add, uint16, +, uint16) arith_op_template(int16, add, int16, +, int16)
arith_op_template(uint8,  add,  uint8, +,  uint8) arith_op_template(int8,  add,  int8, +,  int8)
arith_op_template(float32, add, float32, +, float32) arith_op_template(float64, add, float64, +, float64)

// same subs
arith_op_template(uint64, sub, uint64, -, uint64) arith_op_template(int64, sub, int64, -, int64)
arith_op_template(uint32, sub, uint32, -, uint32) arith_op_template(int32, sub, int32, -, int32)
arith_op_template(uint16, sub, uint16, -, uint16) arith_op_template(int16, sub, int16, -, int16)
arith_op_template(uint8,  sub,  uint8, -,  uint8) arith_op_template(int8,  sub,  int8, -,  int8)
arith_op_template(float32, sub, float32, -, float32) arith_op_template(float64, sub, float64, -, float64)

// same mul
arith_op_template(uint64, mul, uint64, *, uint64) arith_op_template(int64, mul, int64, *, int64)
arith_op_template(uint32, mul, uint32, *, uint32) arith_op_template(int32, mul, int32, *, int32)
arith_op_template(uint16, mul, uint16, *, uint16) arith_op_template(int16, mul, int16, *, int16)
arith_op_template(uint8,  mul,  uint8, *,  uint8) arith_op_template(int8,  mul,  int8, *,  int8)
arith_op_template(float32, mul, float32, *, float32) arith_op_template(float64, mul, float64, *, float64)

// same div
arith_op_template(uint64, div, uint64, /, uint64) arith_op_template(int64, div, int64, /, int64)
arith_op_template(uint32, div, uint32, /, uint32) arith_op_template(int32, div, int32, /, int32)
arith_op_template(uint16, div, uint16, /, uint16) arith_op_template(int16, div, int16, /, int16)
arith_op_template(uint8,  div,  uint8, /,  uint8) arith_op_template(int8,  div,  int8, /,  int8)
arith_op_template(float32, div, float32, /, float32) arith_op_template(float64, div, float64, /, float64)
