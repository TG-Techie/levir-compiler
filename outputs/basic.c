typedef struct content_mod_main_Counter /*prototype*/ content_mod_main_Counter;
typedef struct mod_main_Counter /*prototype*/ *type_mod_main_Counter;
type_mod_main_Counter new_mod_main_Counter(content_mod_main_Counter content) __attribute__ ((always_inline));
type_mod_main_Counter dflt_mod_main_Counter() __attribute__ ((always_inline));
type_mod_main_Counter get_mod_main_Counter(type_mod_main_Counter self) __attribute__ ((always_inline));
void drop_mod_main_Counter(type_mod_main_Counter self) __attribute__ ((always_inline));
void rtn_mod_main_Counter(type_mod_main_Counter self) __attribute__ ((always_inline));
void rel_mod_main_Counter(type_mod_main_Counter self) __attribute__ ((always_inline));
content_mod_main_Counter* cntnptr_mod_main_Counter(type_mod_main_Counter* selfptr) __attribute__ ((always_inline));
type_uint32 fn_main ();
typedef struct content_mod_main_Counter{
    type_uint32 mbr__count;
} content_mod_main_Counter;
struct mod_main_Counter {
    RefCount rc;
    content_mod_main_Counter content;
};
type_mod_main_Counter new_mod_main_Counter(content_mod_main_Counter content){
    type_mod_main_Counter self = (type_mod_main_Counter)malloc(sizeof(struct mod_main_Counter));
    self->rc = 1;
    self->content = content;
    return self;
}
type_mod_main_Counter dflt_mod_main_Counter(){
    return NULL;
}
type_mod_main_Counter get_mod_main_Counter(type_mod_main_Counter self){
    rtn_mod_main_Counter(self);
    return self;
}
void drop_mod_main_Counter(type_mod_main_Counter self){
    rel_mod_main_Counter(self);
    return;
}
void rtn_mod_main_Counter(type_mod_main_Counter self){
    self->rc +=1;
    return;
}
void rel_mod_main_Counter(type_mod_main_Counter self){
    if (self == NULL){return;}
    self->rc -= 1;
    if (self->rc == 0){
        rel_uint32(self->content.mbr__count);
        free(self);
    }
    return;
}
content_mod_main_Counter* cntnptr_mod_main_Counter(type_mod_main_Counter* selfptr){
    type_mod_main_Counter self = *selfptr;
    return &(self->content);
}
type_uint32 fn_main(){ 
    type_mod_main_Counter var_foo = dflt_mod_main_Counter();
    type_uint32 var_foombr1 = dflt_uint32();
    type_uint32 var_foombr2 = dflt_uint32();
    { /* assignment */
        type_mod_main_Counter* target_ptr = &(var_foo);
        type_mod_main_Counter prev_value = *target_ptr;
        *target_ptr = new_mod_main_Counter( (content_mod_main_Counter) {litrl_uint32(6)});
        rel_mod_main_Counter(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(var_foombr1);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = get_uint32(cntnptr_mod_main_Counter(&(var_foo))->mbr__count);
        rel_uint32(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(cntnptr_mod_main_Counter(&(var_foo))->mbr__count);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = litrl_uint32(128);
        rel_uint32(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(var_foombr2);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = get_uint32(cntnptr_mod_main_Counter(&(var_foo))->mbr__count);
        rel_uint32(prev_value);
    }
    /* return statement */
    type_uint32 _return_tmp_ = get_uint32(var_foombr1);
    goto _return_label_;
_return_label_:
    drop_mod_main_Counter(var_foo);
    drop_uint32(var_foombr1);
    drop_uint32(var_foombr2);
    return _return_tmp_;
}
