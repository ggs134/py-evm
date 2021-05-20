from eth.vm.forks.berlin.headers import (
    configure_header,
    create_header_from_parent,
    compute_berlin_difficulty,
)


compute_daejun_difficulty = compute_berlin_difficulty

create_daejun_header_from_parent = create_header_from_parent(
    compute_berlin_difficulty
)
configure_daejun_header = configure_header(compute_daejun_difficulty)
