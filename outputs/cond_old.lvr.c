type_uint32 fn_main ();
type_uint32 fn_main(){ 
    type_Bool var_cond1 = dflt_Bool();
    type_Bool var_cond2 = dflt_Bool();
    type_Bool var_cond3 = dflt_Bool();
    { /* assignment [file:'examples/cond_old.lvr' line:9 col:17] */
        type_Bool* target_ptr = &(var_cond1);
        type_Bool prev_value = *target_ptr;
        *target_ptr = litrl_Bool(True);
        drop_Bool(prev_value);
    }
    if ((get_Bool(var_cond1)).native) {
        puts("True");
    }
    else  {
        puts("False");
    }
    /* return statement */
    type_uint32 _return_tmp_ = litrl_uint32(0);
    goto _return_label_;
_return_label_:
    drop_Bool(var_cond1);
    drop_Bool(var_cond2);
    drop_Bool(var_cond3);
    return _return_tmp_;
}
