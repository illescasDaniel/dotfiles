function _pure_prompt \
    --description 'Print prompt symbol' \
    --argument-names exit_code

    set --local jobs (_pure_prompt_jobs)
    set --local virtualenv (_pure_prompt_virtualenv) # Python virtualenv name
    set --local vimode_indicator (_pure_prompt_vimode) # vi-mode indicator
    set --local pure_symbol (_pure_prompt_symbol $exit_code)
    set --local system_time (_pure_prompt_system_time)

    echo (_pure_print_prompt $system_time $jobs $virtualenv $vimode_indicator $pure_symbol)
end
