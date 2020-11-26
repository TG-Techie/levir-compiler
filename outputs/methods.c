typedef struct Counter /*prototype*/ type_Counter;
typedef type_Counter content_Counter;
type_Counter new_Counter(content_Counter content) __attribute__ ((always_inline));
type_Counter dflt_Counter() __attribute__ ((always_inline));
type_Counter get_Counter(type_Counter self) __attribute__ ((always_inline));
void drop_Counter(type_Counter self) __attribute__ ((always_inline));
void rtn_Counter(type_Counter self) __attribute__ ((always_inline));
void rel_Counter(type_Counter self) __attribute__ ((always_inline));
content_Counter* cntnptr_Counter(type_Counter* selfptr) __attribute__ ((always_inline));
type_Void fn_inc (type_Counter var_self);
type_Void fn_dec (type_Counter var_self);
typedef struct Counter{
    type_uint64 mbr__count;
} content_Counter;
type_Counter new_Counter(content_Counter content){
    return content; // a struct and its content is the same thing}
type_Counter dflt_Counter(){
return (){
        .mbr__count = dflt_type_uint64;
    };
}
type_Void fn_inc(type_Counter var_self){ 
    
    { /* assignment */
        type_uint64* target_ptr = &(cntnptr_Counter(&(var_self))->mbr__count);
        type_uint64 prev_value = *target_ptr;
        *target_ptr = add_uint64_uint64(get_uint64(cntnptr_Counter(&(var_self))->mbr__count), litrl_uint64(1));
        rel_uint64(prev_value);
    }
    /* return statement */
    type_Void _return_tmp_ = litrl_Void(0);
    goto _return_label_;
_return_label_:
    drop_Counter(var_self);
    return _return_tmp_;
}
type_Void fn_dec(type_Counter var_self){ 
    
    { /* assignment */
        type_uint64* target_ptr = &(cntnptr_Counter(&(var_self))->mbr__count);
        type_uint64 prev_value = *target_ptr;
        *target_ptr = sub_uint64_uint64(get_uint64(cntnptr_Counter(&(var_self))->mbr__count), litrl_uint64(1));
        rel_uint64(prev_value);
    }
    /* return statement */
    type_Void _return_tmp_ = litrl_Void(0);
    goto _return_label_;
_return_label_:
    drop_Counter(var_self);
    return _return_tmp_;
}
