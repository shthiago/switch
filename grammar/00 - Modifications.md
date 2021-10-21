# Modificações sobre a gramática original

1. Remover os não-terminais `ConstructQuery`, `DescribeQuery` e `AskQuery` da gramática. Dessa forma, a lingaugem faz apenas leitura de dados, sem escrita, atualização ou deleção.
    Razão: Simplificar a linguagem, removendo produções que precisem ser trabalhadas nos próximos passos. Removendo o não-terminal `ConstructQuery` também elimina-se a capacidade da consulta de retornar grafos explicitamente, mantendo apenas a capacidade de retornar tuplas compostas pelas variáveis definidas na consulta.
2. Remover o não-terminal `DatasetClause`.
    Razão: As consultas em Cypher serão executadas apenas sobre dados previamente carregados, não havendo a possibilidade de carregar dados de fontes externas com `FROM` em SPARQL.
3. Remover o não-terminal `GraphGraphPattern`.
    Razão: Como as consultas não podem trazer dados de grafos além do que está carregado no banco (vide modificação #2), a utilização da palavra-chave `GRAPH` para aplicar consultas sobre determinados sub-grafos importados utilizando `FROM` não é mais possível.
4. Remover o não-terminal `ServiceGraphPattern`.
    Razão: Como a consulta será executada em Cypher sobre dados pré-carregados, a utilização de serviços em SPARQL não é possível.
5. Remover os não-terminais `iriOrFunction` e `FunctionCall`, substituindo a ocorrência de `iriOrFunction` como produção de `PrimaryExpression` por apenas `iri`, mantendo a capacidade deste de derivar para `iri`, agora de forma direta. 
    Razão: Esses não-terminais servem para efetuar chamadas para funções programadas pelo usuário, na forma de extensões. Inicialmente essa funcionalidade não entrará na conversão por conta da complexidade de implementação.
6. Remover as chamadas para as funções/operadores abaixo:
    `STRBEFORE`, `STRAFTER`, `ENCODE_FOR_URI`, `LANGMATCHES`, `SAMPLE`, `GROUP_CONCAT`, `EXISTS`, `NOT EXISTS`,  `sameTerm`, `isIRI`, `isURI`, `isBLANK`, `isLITERAL`, `isNUMERIC`, `STR`, `LANG`, `DATATYPE`, `IRI`, `URI`, `BNODE`, `STRDT`, `STRLANG`, `UUID`, `STRUUID`, `BOUND`, `IF`, `MD5`, `SHA1`, `SHA256`, `SHA384`, `SHA51`.
    Consequentemente, removendo os não-terminais `ExistsFunc` e `NotExistsFunc`.
    Razão: Essas funções/operadores são específicas da linguagem SPARQL e/ou não tem correspondência direta com alguma função padrão de Cypher.
7. Remover o não-terminal `SubSelect`.
    Razão: Simplificar a linguagem
8. Remover não-terminais não utilizados no corpo de alguma produção.
    `Load`, `DeleteClause`, `GraphOrDefault`, `NamedGraphClause`, `DeleteData`, `Clear`, `Update1`, `Drop`, `ConstructTriples`, `Update`, `TriplesTemplate`, `ConstructTemplate`, `Copy`, `Add`, `InsertClause`, `Quads`, `DefaultGraphClause`, `GraphRefAll`, `TriplesSameSubject`, `ArgList`, `UsingClause`, `GraphRef`, `Move`, `Modify`, `Integer`, `DeleteWhere`, `UpdateUnit`, `QuadsNotTriples`, `QuadPattern`, `Create`, `InsertData`, `QuadData`, `SourceSelector`, `PropertyList`
9. Normalizar as produções, substituindo as notações *, + e ? por novas produções que expressem a intenção porém apenas com produções simples.
    Razão: Ficará mais fácil de estabelecer as ações semânticas.