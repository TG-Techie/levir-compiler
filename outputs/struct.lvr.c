typedef struct Point /*prototype*/ type_Point;
typedef type_Point content_Point;
type_Point new_Point(content_Point content) __attribute__ ((always_inline));
type_Point dflt_Point() __attribute__ ((always_inline));
type_Point get_Point(type_Point self) __attribute__ ((always_inline));
void drop_Point(type_Point self) __attribute__ ((always_inline));
void rtn_Point(type_Point self) __attribute__ ((always_inline));
void rel_Point(type_Point self) __attribute__ ((always_inline));
content_Point* cntnptr_Point(type_Point* selfptr) __attribute__ ((always_inline));
type_float64 fn_main ();
typedef struct Point{
    type_float64 mbr_x;
    type_float64 mbr_y;
} content_Point;
type_Point new_Point(content_Point content){
    return content; /* a struct and its content is the same thing*/
}
type_Point dflt_Point(){
    return (type_Point) {
        .mbr_x = dflt_float64(),
        .mbr_y = dflt_float64(),
    };
}
type_Point get_Point(type_Point self){
    return (type_Point){
        .mbr_x = get_float64(self.mbr_x),
        .mbr_y = get_float64(self.mbr_y),
    };
}
void drop_Point(type_Point self){
    drop_float64(self.mbr_x);
    drop_float64(self.mbr_y);
    return;
}
void rtn_Point(type_Point self){
    return;
}
void rel_Point(type_Point self){
    return;
}
content_Point* cntnptr_Point(type_Point* selfptr){
    return (content_Point*) selfptr;
}
type_float64 fn_main(){ 
    type_Point var_init = dflt_Point();
    type_Point var_copy = dflt_Point();
    type_float64 var_xinit = dflt_float64();
    type_float64 var_xcopy = dflt_float64();
    { /* assignment [file:'examples/struct.lvr' line:14 col:17] */
        type_Point* target_ptr = &(var_init);
        type_Point prev_value = *target_ptr;
        *target_ptr = new_Point( (content_Point) {litrl_float64(0.0), litrl_float64(0.0)});
        drop_Point(prev_value);
    }
    { /* assignment [file:'examples/struct.lvr' line:21 col:17] */
        type_Point* target_ptr = &(var_copy);
        type_Point prev_value = *target_ptr;
        *target_ptr = get_Point(var_init);
        drop_Point(prev_value);
    }
    { /* assignment [file:'examples/struct.lvr' line:26 col:19] */
        type_float64* target_ptr = &(cntnptr_Point(&(var_copy))->mbr_x);
        type_float64 prev_value = *target_ptr;
        *target_ptr = litrl_float64(7.0);
        drop_float64(prev_value);
    }
    { /* assignment [file:'examples/struct.lvr' line:31 col:17] */
        type_float64* target_ptr = &(var_xinit);
        type_float64 prev_value = *target_ptr;
        *target_ptr = get_float64(cntnptr_Point(&(var_init))->mbr_x);
        drop_float64(prev_value);
    }
    { /* assignment [file:'examples/struct.lvr' line:35 col:17] */
        type_float64* target_ptr = &(var_xcopy);
        type_float64 prev_value = *target_ptr;
        *target_ptr = get_float64(cntnptr_Point(&(var_copy))->mbr_x);
        drop_float64(prev_value);
    }
    /* return statement */
    type_float64 _return_tmp_ = litrl_float64(0.0);
    goto _return_label_;
_return_label_:
    drop_Point(var_init);
    drop_Point(var_copy);
    drop_float64(var_xinit);
    drop_float64(var_xcopy);
    return _return_tmp_;
}
