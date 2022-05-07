from transpiler.parser import SelectSparqlParser

if __name__ == "__main__":
    parser = SelectSparqlParser()
    result = parser.parse("SELECT * WHERE { ?s ?p ?o }")

    print(result)
