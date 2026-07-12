# Episode 002 Internal Review Limitations

このmilestoneはmedia-validな内部review packageです。以下の3件は意図的に未解決です。

| debt_id | issue | impact | owner | revisit_trigger | status |
| --- | --- | --- | --- | --- | --- |
| D1 | Visual/editorial acceptance remains human review debt. | Machine decode cannot establish readability, timing feel, or editorial quality. | Human reviewer | Before H2 merge-ready acceptance or any creative-final claim. | open |
| D2 | Character profile 4.53.0.9 differs from observed YMM4 4.54.0.1. | This run reported no mapping error, but a future environment may map differently. | Operator/batch maintainer | Any YMM4/profile change, mapping dialog, or character mismatch. | accepted debt |
| D3 | The ignored local project contains machine-local asset references. | The `.local.ymmp` is not guaranteed to open unchanged on another machine. | Future portability slice | Cross-machine transfer, production adoption, or portable project packaging. | accepted debt |

The proxy improves reviewability but does not replace or alter the immutable original. Rights/legal approval, production project creation, upload/publication, and default-branch integration remain outside this milestone.
