typedef struct content_Point /*prototype*/ content_Point;
typedef struct Point /*prototype*/ *type_Point;
type_Point new_Point(content_Point content) __attribute__ ((always_inline));
type_Point dflt_Point() __attribute__ ((always_inline));
type_Point get_Point(type_Point self) __attribute__ ((always_inline));
void drop_Point(type_Point self) __attribute__ ((always_inline));
void rtn_Point(type_Point self) __attribute__ ((always_inline));
void rel_Point(type_Point self) __attribute__ ((always_inline));
content_Point* cntnptr_Point(type_Point* selfptr) __attribute__ ((always_inline));
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
typedef struct content_Point{
    type_uint32 mbr_x;
    type_uint32 mbr_y;
} content_Point;
struct Point {
    RefCount rc;
    content_Point content;
};
type_Point new_Point(content_Point content){
    type_Point self = (type_Point)malloc(sizeof(struct Point));
    self->rc = 1;
    self->content = content;
    return self;
}
type_Point dflt_Point(){
    return NULL;
}
type_Point get_Point(type_Point self){
    rtn_Point(self);
    return self;
}
void drop_Point(type_Point self){
    rel_Point(self);
    return;
}
void rtn_Point(type_Point self){
    self->rc +=1;
    return;
}
void rel_Point(type_Point self){
    if (self == NULL){return;}
    self->rc -= 1;
    if (self->rc == 0){
        rel_uint32(self->content.mbr_x);
        rel_uint32(self->content.mbr_y);
        free(self);
    }
    return;
}
content_Point* cntnptr_Point(type_Point* selfptr){
    type_Point self = *selfptr;
    return &(self->content);
}
typedef struct content_Widget{
    type_Point mbr_coord;
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
        rel_Point(self->content.mbr_coord);
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
    type_Point var_first = dflt_Point();
    type_Point var_second = dflt_Point();
    type_uint32 var_x = dflt_uint32();
    { /* assignment */
        type_Point* target_ptr = &(var_first);
        type_Point prev_value = *target_ptr;
        *target_ptr = new_Point( (content_Point) {litrl_uint32(0), litrl_uint32(0)});
        rel_Point(prev_value);
    }
    { /* assignment */
        type_Point* target_ptr = &(var_second);
        type_Point prev_value = *target_ptr;
        *target_ptr = new_Point( (content_Point) {litrl_uint32(127), litrl_uint32(255)});
        rel_Point(prev_value);
    }
    { /* assignment */
        type_Widget* target_ptr = &(var_button);
        type_Widget prev_value = *target_ptr;
        *target_ptr = new_Widget( (content_Widget) {get_Point(var_first)});
        rel_Widget(prev_value);
    }
    { /* assignment */
        type_Point* target_ptr = &(cntnptr_Widget(&(var_button))->mbr_coord);
        type_Point prev_value = *target_ptr;
        *target_ptr = get_Point(var_second);
        rel_Point(prev_value);
    }
    { /* assignment */
        type_uint32* target_ptr = &(cntnptr_Point(&(cntnptr_Widget(&(var_button))->mbr_coord))->mbr_y);
        type_uint32 prev_value = *target_ptr;
        *target_ptr = litrl_uint32(0);
        rel_uint32(prev_value);
    }
    /* return statement */
    type_uint32 _return_tmp_ = litrl_uint32(0);
    goto _return_label_;
_return_label_:
    drop_Widget(var_button);
    drop_Point(var_first);
    drop_Point(var_second);
    drop_uint32(var_x);
    return _return_tmp_;
}
