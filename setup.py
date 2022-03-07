import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SwiftDoc",
    version="2.0",
    description="Web Interface Driven Configuration Converter from Security Elements to Deliverable Documentation",
    author=["Anton Coleman", "Satwik Satat", "Ravi Budhwar", "Vaibhav Jain", "Franklin Diaz"],
    author_email=[
        "ssatat@paloaltonetworks.com",
        "rbudhwar@paloaltonetworks.com",
        "vaijain@paloaltonetworks.com",
        "acoleman@paloaltonetworks.com",
        "fdiaz@paloaltonetworks.com",
    ],
    url="https://github.com/ancoleman/ps-swiftodc-2.0",
    python_requires=">=3.8.1",
    extras_require={"test": ["pytest"]},
)
