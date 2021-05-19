from eth.vm.forks.berlin.headers import (
    configure_header,
    create_header_from_parent,
    compute_berlin_difficulty,
)


compute_seoul_difficulty = compute_berlin_difficulty

create_seoul_header_from_parent = create_header_from_parent(
    compute_berlin_difficulty
)
configure_seoul_header = configure_header(compute_seoul_difficulty)
