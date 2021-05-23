from eth.vm.forks.berlin.headers import (
    configure_header,
    create_header_from_parent,
    compute_berlin_difficulty,
)


compute_busan_difficulty = compute_berlin_difficulty

create_busan_header_from_parent = create_header_from_parent(
    compute_berlin_difficulty
)
configure_busan_header = configure_header(compute_busan_difficulty)
