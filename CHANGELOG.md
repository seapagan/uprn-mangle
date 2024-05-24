# Changelog

This is an auto-generated log of all the changes that have been made to the
project since the first release, with the latest changes at the top.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased](https://github.com/seapagan/uprn-mangle/tree/HEAD)


These are the changes that have been merged to the repository since the last
release. If you want to try out these changes, you can install the latest
version from the main branch by running:

```console
$ pip install git+https://github.com/seapagan/github-changelog-md
```

or, if using poetry:

```console
$ poetry add git+https://github.com/seapagan/github-changelog-md
```
Everything in this section will be included in the next official release.


**New Features**

- Optimize phase 3 - rewrite from scratch ([#249](https://github.com/seapagan/uprn-mangle/pull/249)) by [seapagan](https://github.com/seapagan)
- Optimize phase 2, use parquet files to reduce memory usage ([#247](https://github.com/seapagan/uprn-mangle/pull/247)) by [seapagan](https://github.com/seapagan)
- Add settings file ([#246](https://github.com/seapagan/uprn-mangle/pull/246)) by [seapagan](https://github.com/seapagan)
- Refactor app to use `Poetry` and start optimizing Phase 1 & 2 ([#227](https://github.com/seapagan/uprn-mangle/pull/227)) by [seapagan](https://github.com/seapagan)
- Try to tidy and optimize the CSV conversion stage. ([#82](https://github.com/seapagan/uprn-mangle/pull/82)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Refactor the layout for database access and models ([#252](https://github.com/seapagan/uprn-mangle/pull/252)) by [seapagan](https://github.com/seapagan)
- Refactor and tidy the overall code ([#250](https://github.com/seapagan/uprn-mangle/pull/250)) by [seapagan](https://github.com/seapagan)

[`Full Changelog`](https://github.com/seapagan/uprn-mangle/compare/0.1.0...HEAD) | [`Diff`](https://github.com/seapagan/uprn-mangle/compare/0.1.0...HEAD.diff) | [`Patch`](https://github.com/seapagan/uprn-mangle/compare/0.1.0...HEAD.patch)

## [0.1.0](https://github.com/seapagan/uprn-mangle/releases/tag/0.1.0) (June 15, 2023)

**_'Legacy Release'_**

**Merged Pull Requests**

- Upgrade to Django 4 ([#41](https://github.com/seapagan/uprn-mangle/pull/41)) by [seapagan](https://github.com/seapagan)
- Db to env ([#13](https://github.com/seapagan/uprn-mangle/pull/13)) by [seapagan](https://github.com/seapagan)
- Refactor ([#12](https://github.com/seapagan/uprn-mangle/pull/12)) by [seapagan](https://github.com/seapagan)
- Create LICENSE ([#3](https://github.com/seapagan/uprn-mangle/pull/3)) by [seapagan](https://github.com/seapagan)
- Add skeleton front end and tidy backend functionality ([#2](https://github.com/seapagan/uprn-mangle/pull/2)) by [seapagan](https://github.com/seapagan)
- Webapp - backend ([#1](https://github.com/seapagan/uprn-mangle/pull/1)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump webpack from 5.73.0 to 5.87.0 in /frontend ([#167](https://github.com/seapagan/uprn-mangle/pull/167)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump react-icons from 4.6.0 to 4.8.0 in /frontend ([#166](https://github.com/seapagan/uprn-mangle/pull/166)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump dns-packet from 5.3.1 to 5.4.0 in /frontend ([#165](https://github.com/seapagan/uprn-mangle/pull/165)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Update ipython requirement from <8.7.0,>=8.4.0 to >=8.4.0,<8.12.0 in /backend ([#164](https://github.com/seapagan/uprn-mangle/pull/164)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump eslint from 8.28.0 to 8.35.0 in /frontend ([#163](https://github.com/seapagan/uprn-mangle/pull/163)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Update python-dotenv requirement from <0.22.0,>=0.19.1 to >=0.19.1,<1.1.0 in /backend ([#162](https://github.com/seapagan/uprn-mangle/pull/162)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump sass from 1.56.1 to 1.58.3 in /frontend ([#161](https://github.com/seapagan/uprn-mangle/pull/161)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump @testing-library/react from 13.4.0 to 14.0.0 in /frontend ([#159](https://github.com/seapagan/uprn-mangle/pull/159)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Update newrelic requirement from <8.5.0,>=7.2.2 to >=7.2.2,<8.8.0 in /backend ([#158](https://github.com/seapagan/uprn-mangle/pull/158)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Update pytest-xdist requirement from <3.1.0,>=2.4.0 to >=2.4.0,<3.3.0 in /backend ([#153](https://github.com/seapagan/uprn-mangle/pull/153)) by [dependabot[bot]](https://github.com/apps/dependabot)
- *and 64 more dependency updates*

---
*This changelog was generated using [github-changelog-md](http://changelog.seapagan.net/) by [Seapagan](https://github.com/seapagan)*
