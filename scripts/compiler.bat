@call %1
@pushd %2
@devenv %3 /build %4 /project %5 > %6 2>&1
@popd