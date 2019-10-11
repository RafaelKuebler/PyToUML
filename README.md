# PyToUML

Automatically generates UML class diagrams from python source code.
Makes use of the [ast](https://docs.python.org/3/library/ast.html) python module to analyze
the source's abstract syntax tree and extract information about
classes, class variables, class docstrings, functions and class inheritance relationships.
The UML class diagram is then generated using PlantUML.

## Example
The UML class diagram was generated from the own source code.

<img alt="UML class diagram from own source" src="https://user-images.githubusercontent.com/9216979/66649207-e3244800-ec2d-11e9-87e8-46634b65975e.png">

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
