# How to contribute

Thanks for contributing to `attack-control-framework-mappings`!

Mapping security controls to ATT&CK can be a subjective process and we welcome your feedback on our current work as well as your contributions to expand upon this repository of control mappings to ATT&CK. 

You are welcome to comment on issues, open new issues, and open pull requests.

Pull requests should target the **develop** branch of the repository.

## Types of contributions

### Feedback or questions on the methodology

Users wishing to submit feedback or questions on the methodology mappings should submit issues. 

### New mappings to an existing framework

Please submit new issues if you wish to contribute additional mappings to a security control framework that is already included in this project. This will increase transparency for the project as we review your contributions. 

### New Control Frameworks

- Coordinate - Mapping a control frameworks takes significant time and effort. Email us at ctid@mitre-engenuity.org to help us ensure that our control framework mapping work is well coordinated. 
- Location - You may contribute new control frameworks within the `frameworks/` folder. 
- Format - Contributions of control frameworks and associated mappings should follow the format outlined in the [README](README.md#output-data), extended with additional `x_mitre_` properties when relevant. 
- Reuse - We encourage you to reuse the existing mappings parser if possible.

### Improvements to an existing framework parser

You're welcome to contribute improvements to the existing framework parsers. Such contributions may  (for example):
- Formatting improvements to the output control STIX content
- Support for additional control `x_mitre_` fields or relationships

### New Framework-Agnostic Tools or Utilities

Framework-agnostic tools and utilities may be added within the `src/` folder. 
- Such contributions should be framework agnostic: avoid hardcoded assumptions about which `x_mitre_` fields exist on the input framework since new frameworks may be added which don't implement common fields such as `x_mitre_family`.
- If your utility is only relevant to certain control frameworks, you should instead put it in the framework directory next to the parser for the framework.

### All other questions and comments

You may contact us at ctid@mitre-engenuity.org for all other questions and comments. 

## Developer's Certificate of Origin v1.1
If you contribute any source code, we need you to agree to the following Developer's Certificate of Origin below.

```
By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```
