#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// TODO: auto generate macros for each individual possible operation and type.
//  this leaves the definition of optionals (etc) and checkedcasting into a
//  lang implementor issue.

#define number_template(typename, nativetype) \
    typedef struct { nativetype native; } type_##typename; \
    type_##typename __attribute__((always_inline)) dflt_##typename () \
        { return (type_##typename){0}; } \
    type_##typename __attribute__((always_inline)) get_##typename (type_##typename self) \
        { return self; } \
    void __attribute__((always_inline)) drop_##typename (type_##typename self) \
        { return; } \
    void __attribute__((always_inline)) rtn_##typename (type_##typename self) \
        { return; } \
    void __attribute__((always_inline)) rel_##typename (type_##typename self) \
        { return; } \
    type_##typename __attribute__((always_inline)) litrl_##typename (nativetype val) \
        { return (type_##typename){val}; } \

    // cntn expose not required

#define arith_op_template(outtype, opname, atype, nativeop, btype) \
    type_##outtype opname##_##atype##_##btype (type_##atype a, type_##btype b) { \
        return (type_##outtype) { a.native nativeop b.native}; \
    }

#define cast_template(totype, fromtype) \
    type_##totype cast_##fromtype##_to_##totype (type_##fromtype val) { \
        return (type_##totype) { val.native };\
    }


typedef struct {
    bool native;
} type_bool;

// literal definition
bool False = false;
bool True = true;

type_bool __attribute__((always_inline)) litrl_bool(bool val) {
    return (type_bool){val};
}
type_bool __attribute__((always_inline)) dflt_bool() {
    return (type_bool){false};
}
type_bool __attribute__((always_inline)) get_bool(type_bool self) {
    return self; // copy
}
void __attribute__((always_inline)) drop_bool(type_bool self) {
    return;
}
void __attribute__((always_inline)) rtn_bool(type_bool self) {
    return;
}
void __attribute__((always_inline)) rel_bool(type_bool self) {
    return;
}

typedef struct {} type_Nothing;

type_Nothing none = {};

type_Nothing __attribute__((always_inline)) litrl_Nothing(type_Nothing _none) {
    return (type_Nothing){};
}
type_Nothing __attribute__((always_inline)) dflt_Nothing() {
    return (type_Nothing){};
}
type_Nothing __attribute__((always_inline)) get_Nothing(type_Nothing self) {
    return (type_Nothing){}; // copy
}
void __attribute__((always_inline)) drop_Nothing(type_Nothing self) {
    return;
}
void __attribute__((always_inline)) rtn_Nothing(type_Nothing self) {
    return;
}
void __attribute__((always_inline)) rel_Nothing(type_Nothing self) {
    return;
}


// bases
typedef uint64_t RefCount;

number_template(usize,  uint64_t)
number_template(RefCount,  uint64_t)

number_template(u64, uint64_t)
number_template(u32, uint32_t)
number_template(u16, uint16_t)
number_template(u8,  uint8_t)

number_template(i64, int64_t)
number_template(i32, int32_t)
number_template(i16, int16_t)
number_template(i8,  int8_t)

number_template(f32, float)
number_template(f64, double)

cast_template(u64, u32) cast_template(i64, i32)
cast_template(u64, u16) cast_template(i64, i16)
cast_template(u64,  u8) cast_template(i64,  i8)

cast_template(u32, u16) cast_template(i32, i16)
cast_template(u32,  u8) cast_template(i32,  i8)

cast_template(u16,  u8) cast_template(i16,  i8)

cast_template(f64, f32)

// same adds
arith_op_template(u64, add, u64, +, u64) arith_op_template(i64, add, i64, +, i64)
arith_op_template(u32, add, u32, +, u32) arith_op_template(i32, add, i32, +, i32)
arith_op_template(u16, add, u16, +, u16) arith_op_template(i16, add, i16, +, i16)
arith_op_template(u8,  add,  u8, +,  u8) arith_op_template(i8,  add,  i8, +,  i8)
arith_op_template(f32, add, f32, +, f32) arith_op_template(f64, add, f64, +, f64)

// same subs
arith_op_template(u64, sub, u64, -, u64) arith_op_template(i64, sub, i64, -, i64)
arith_op_template(u32, sub, u32, -, u32) arith_op_template(i32, sub, i32, -, i32)
arith_op_template(u16, sub, u16, -, u16) arith_op_template(i16, sub, i16, -, i16)
arith_op_template(u8,  sub,  u8, -,  u8) arith_op_template(i8,  sub,  i8, -,  i8)
arith_op_template(f32, sub, f32, -, f32) arith_op_template(f64, sub, f64, -, f64)

// same mul
arith_op_template(u64, mul, u64, *, u64) arith_op_template(i64, mul, i64, *, i64)
arith_op_template(u32, mul, u32, *, u32) arith_op_template(i32, mul, i32, *, i32)
arith_op_template(u16, mul, u16, *, u16) arith_op_template(i16, mul, i16, *, i16)
arith_op_template(u8,  mul,  u8, *,  u8) arith_op_template(i8,  mul,  i8, *,  i8)
arith_op_template(f32, mul, f32, *, f32) arith_op_template(f64, mul, f64, *, f64)

// same div
arith_op_template(u64, div, u64, /, u64) arith_op_template(i64, div, i64, /, i64)
arith_op_template(u32, div, u32, /, u32) arith_op_template(i32, div, i32, /, i32)
arith_op_template(u16, div, u16, /, u16) arith_op_template(i16, div, i16, /, i16)
arith_op_template(u8,  div,  u8, /,  u8) arith_op_template(i8,  div,  i8, /,  i8)
arith_op_template(f32, div, f32, /, f32) arith_op_template(f64, div, f64, /, f64)
