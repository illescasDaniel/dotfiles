function _pure_prompt_ssh_host
    set --local hostname_color (_pure_set_color $pure_color_ssh_hostname)

    echo "$hostname_color$hostname"
end
