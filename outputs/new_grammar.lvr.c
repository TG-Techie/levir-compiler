typedef struct content_Coord /*prototype*/ content_Coord;
typedef struct Coord /*prototype*/ *type_Coord;
type_Coord new_Coord(content_Coord content) __attribute__ ((always_inline));
type_Coord dflt_Coord() __attribute__ ((always_inline));
type_Coord get_Coord(type_Coord self) __attribute__ ((always_inline));
void drop_Coord(type_Coord self) __attribute__ ((always_inline));
void rtn_Coord(type_Coord self) __attribute__ ((always_inline));
void rel_Coord(type_Coord self) __attribute__ ((always_inline));
content_Coord* cntnptr_Coord(type_Coord* selfptr) __attribute__ ((always_inline));
typedef struct content_Widget /*prototype*/ content_Widget;
typedef struct Widget /*prototype*/ *type_Widget;
type_Widget new_Widget(content_Widget content) __attribute__ ((always_inline));
type_Widget dflt_Widget() __attribute__ ((always_inline));
type_Widget get_Widget(type_Widget self) __attribute__ ((always_inline));
void drop_Widget(type_Widget self) __attribute__ ((always_inline));
void rtn_Widget(type_Widget self) __attribute__ ((always_inline));
void rel_Widget(type_Widget self) __attribute__ ((always_inline));
content_Widget* cntnptr_Widget(type_Widget* selfptr) __attribute__ ((always_inline));
type_uint32 fn_main ();
typedef struct content_Coord{
    type_uint32 mbr_x;
    type_uint32 mbr_y;
} content_Coord;
struct Coord {
    RefCount rc;
    content_Coord content;
};
type_Coord new_Coord(content_Coord content){
    type_Coord self = (type_Coord)malloc(sizeof(struct Coord));
    self->rc = 1;
    self->content = content;
    return self;
}
type_Coord dflt_Coord(){
    return NULL;
}
type_Coord get_Coord(type_Coord self){
    rtn_Coord(self);
    return self;
}
void drop_Coord(type_Coord self){
    rel_Coord(self);
    return;
}
void rtn_Coord(type_Coord self){
    self->rc +=1;
    return;
}
void rel_Coord(type_Coord self){
    if (self == NULL){return;}
    self->rc -= 1;
    if (self->rc == 0){
        rel_uint32(self->content.mbr_x);
        rel_uint32(self->content.mbr_y);
        free(self);
    }
    return;
}
content_Coord* cntnptr_Coord(type_Coord* selfptr){
    type_Coord self = *selfptr;
    return &(self->content);
}
typedef struct content_Widget{
    type_Coord mbr_pos;
} content_Widget;
struct Widget {
    RefCount rc;
    content_Widget content;
};
type_Widget new_Widget(content_Widget content){
    type_Widget self = (type_Widget)malloc(sizeof(struct Widget));
    self->rc = 1;
    self->content = content;
    return self;
}
type_Widget dflt_Widget(){
    return NULL;
}
type_Widget get_Widget(type_Widget self){
    rtn_Widget(self);
    return self;
}
void drop_Widget(type_Widget self){
    rel_Widget(self);
    return;
}
void rtn_Widget(type_Widget self){
    self->rc +=1;
    return;
}
void rel_Widget(type_Widget self){
    if (self == NULL){return;}
    self->rc -= 1;
    if (self->rc == 0){
        rel_Coord(self->content.mbr_pos);
        free(self);
    }
    return;
}
content_Widget* cntnptr_Widget(type_Widget* selfptr){
    type_Widget self = *selfptr;
    return &(self->content);
}
type_uint32 fn_main(){ 
    type_Widget var_button = dflt_Widget();
    type_Coord var_first = dflt_Coord();
    type_Coord var_second = dflt_Coord();
    type_uint32 var_x = dflt_uint32();
    type_uint32 var_overwrite = dflt_uint32();
    { /* assignment */
        type_Coord* target_ptr = &(var_first);
        type_Coord prev_value = *target_ptr;
        *target_ptr = new_Coord( (content_Coord) {litrl_uint32(0)});
        rel_Coord(prev_value);
    }
    { /* assignment */
        type_Coord* target_ptr = &(var_second);
        type_Coord prev_value = *target_ptr;
        *target_ptr = new_Coord( (content_Coord) {litrl_uint32(127)});
        rel_Coord(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(var_overwrite);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = litrl_uint32(511);
        rel_uint32(prev_value);
    }
    { /* assignment */
        type_Widget* target_ptr = &(var_button);
        type_Widget prev_value = *target_ptr;
        *target_ptr = new_Widget( (content_Widget) {get_Coord(var_first)});
        rel_Widget(prev_value);
    }
    { /* assignment */
        type_Coord* target_ptr = &(cntnptr_Widget(&(var_button))->mbr_pos);
        type_Coord prev_value = *target_ptr;
        *target_ptr = get_Coord(var_second);
        rel_Coord(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(cntnptr_Coord(&(cntnptr_Widget(&(var_button))->mbr_pos))->mbr_y);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = get_uint32(var_overwrite);
        rel_uint32(prev_value);
    }
    /* return statement */
    type_uint32 _return_tmp_ = litrl_uint32(0);
    goto _return_label_;
_return_label_:
    drop_Widget(var_button);
    drop_Coord(var_first);
    drop_Coord(var_second);
    drop_uint32(var_x);
    drop_uint32(var_overwrite);
    return _return_tmp_;
}
