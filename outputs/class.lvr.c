typedef struct content_mod_main_Counter /*prototype*/ content_mod_main_Counter;
typedef struct mod_main_Counter /*prototype*/ *type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)});
type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) new_mod_main_Counter(content_mod_main_Counter content) __attribute__ ((always_inline));
type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) dflt_mod_main_Counter() __attribute__ ((always_inline));
type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) get_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self) __attribute__ ((always_inline));
void drop_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self) __attribute__ ((always_inline));
void rtn_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self) __attribute__ ((always_inline));
void rel_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self) __attribute__ ((always_inline));
content_mod_main_Counter* cntnptr_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)})* selfptr) __attribute__ ((always_inline));
type_uint32 fn_main ();
typedef struct content_mod_main_Counter{
    type_uint32 mbr__count;
} content_mod_main_Counter;
struct mod_main_Counter {
    RefCount rc;
    content_mod_main_Counter content;
};
type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) new_mod_main_Counter(content_mod_main_Counter content){
    type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self = (type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}))malloc(sizeof(struct mod_main_Counter));
    self->rc = 1;
    self->content = content;
    return self;
}
type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) dflt_mod_main_Counter(){
    return NULL;
}
type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) get_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self){
    rtn_mod_main_Counter(self);
    return self;
}
void drop_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self){
    rel_mod_main_Counter(self);
    return;
}
void rtn_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self){
    self->rc +=1;
    return;
}
void rel_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self){
    if (self == NULL){return;}
    self->rc -= 1;
    if (self->rc == 0){
        rel_uint32(self->content.mbr__count);
        free(self);
    }
    return;
}
content_mod_main_Counter* cntnptr_mod_main_Counter(type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)})* selfptr){
    type_Class(loc=Location('examples/class.lvr', 6, 7), name='mod_main_Counter', mbrs={'_count': TypeIdent.type(loc=Location('examples/class.lvr', 7, 17), type=BuiltinStruct(name='uint32'), _by_ref=False, _resolved=False, _checked=False)}) self = *selfptr;
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
        drop_mod_main_Counter(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(var_foombr1);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = get_uint32(cntnptr_mod_main_Counter(&(var_foo))->mbr__count);
        drop_uint32(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(cntnptr_mod_main_Counter(&(var_foo))->mbr__count);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = litrl_uint32(128);
        drop_uint32(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(var_foombr2);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = get_uint32(cntnptr_mod_main_Counter(&(var_foo))->mbr__count);
        drop_uint32(prev_value);
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
