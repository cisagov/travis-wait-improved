# travis-wait-improved 👷🏻‍⏲👍 #

[![Build Status](https://travis-ci.com/cisagov/travis-wait-improved.svg?branch=develop)](https://travis-ci.com/cisagov/travis-wait-improved)
[![Coverage Status](https://coveralls.io/repos/github/cisagov/travis-wait-improved/badge.svg?branch=develop)](https://coveralls.io/github/cisagov/travis-wait-improved?branch=develop)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/travis-wait-improved.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/travis-wait-improved/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/travis-wait-improved.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/travis-wait-improved/context:python)
[![Known Vulnerabilities](https://snyk.io/test/github/cisagov/travis-wait-improved/develop/badge.svg)](https://snyk.io/test/github/cisagov/travis-wait-improved)

`travis-wait-improved` is a tool to prevent Travis-CI from thinking a
long-running process has stalled.  It will start a child process,
and pass its output through along with keep-alive messages.

For example, if you wanted to run a packer build that could take up
to 30 minutes, you would add the following to your `.travis.yml` file:

```yml
before_deploy:
  - pip install travis-wait-improved

deploy:
  - provider: script
    script: travis-wait-improved --timeout 30m packer build packer.json
```

## Contributing ##

We welcome contributions!  Please see [here](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
