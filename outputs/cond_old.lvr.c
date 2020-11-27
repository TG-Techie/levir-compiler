type_uint32 fn_main ();
type_uint32 fn_main(){ 
    type_bool var_cond1 = dflt_bool();
    type_bool var_cond2 = dflt_bool();
    type_bool var_cond3 = dflt_bool();
    { /* assignment [file:'examples/cond_old.lvr' line:9 col:17] */
        type_bool* target_ptr = &(var_cond1);
        type_bool prev_value = *target_ptr;
        *target_ptr = litrl_bool(True);
        drop_bool(prev_value);
    }
    if ((get_bool(var_cond1)).native) {
        puts("True");
    }
    else  {
        puts("False");
    }
    /* return statement */
    type_uint32 _return_tmp_ = litrl_uint32(0);
    goto _return_label_;
_return_label_:
    drop_bool(var_cond1);
    drop_bool(var_cond2);
    drop_bool(var_cond3);
    return _return_tmp_;
}
