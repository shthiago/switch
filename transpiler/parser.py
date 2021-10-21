from ply import yacc

from .lexer import SelectSparqlLexer


class SelectSparqlParser:
    def __init__(self, **kwargs):
        self.lexer = SelectSparqlLexer()
        self.tokens = self.lexer.tokens

        self.yacc = yacc.yacc(module=self,
                              check_recursion=False,
                              **kwargs)

    def parse(self, source_code: str) -> str:
        return self.yacc.parse(source_code, lexer=self.lexer)

    def p_production_0(self, p):
        """QueryUnit ::= Query"""
        # TODO

    def p_production_2(self, p):
        """Query ::= Prologue SelectQuery ValuesClause"""
        # TODO

    def p_production_4(self, p):
        """Prologue ::= BaseDecl Prologue"""
        # TODO

    def p_production_5(self, p):
        """Prologue ::= PrefixDecl Prologue"""
        # TODO

    def p_production_6(self, p):
        """Prologue ::= empty"""
        # TODO

    def p_production_8(self, p):
        """BaseDecl ::= KW_BASE IRIREF"""
        # TODO

    def p_production_11(self, p):
        """PrefixDecl ::= KW_PREFIX PNAME_NS IRIREF"""
        # TODO

    def p_production_13(self, p):
        """SelectQuery ::= SelectClause WhereClause SolutionModifier"""
        # TODO

    def p_production_15(self, p):
        """SelectClause ::= KW_SELECT SelectClauseAux1"""
        # TODO

    def p_production_16(self, p):
        """SelectClauseAux1 ::= SelectClauseAux2"""
        # TODO

    def p_production_17(self, p):
        """SelectClauseAux1 ::= KW_DISTINCT SelectClauseAux2"""
        # TODO

    def p_production_18(self, p):
        """SelectClauseAux1 ::= KW_REDUCED SelectClauseAux2"""
        # TODO

    def p_production_19(self, p):
        """SelectClauseAux2 ::= SYMB_ASTERISK"""
        # TODO

    def p_production_20(self, p):
        """SelectClauseAux2 ::= Var SelectClauseAux3"""
        # TODO

    def p_production_21(self, p):
        """SelectClauseAux2 ::= SYMB_LP Expression KW_AS Var SYMB_RP SelectClauseAux3"""
        # TODO

    def p_production_22(self, p):
        """SelectClauseAux3 ::= Var SelectClauseAux3"""
        # TODO

    def p_production_23(self, p):
        """SelectClauseAux3 ::= SYMB_LP Expression KW_AS Var SYMB_RP SelectClauseAux3"""
        # TODO

    def p_production_24(self, p):
        """SelectClauseAux3 ::= empty"""
        # TODO

    def p_production_26(self, p):
        """WhereClause ::= GroupGraphPattern"""
        # TODO

    def p_production_27(self, p):
        """WhereClause ::= KW_WHERE GroupGraphPattern"""
        # TODO

    def p_production_29(self, p):
        """SolutionModifier ::= SolutionModifierAux1 SolutionModifierAux2 SolutionModifierAux3 SolutionModifierAux4"""
        # TODO

    def p_production_30(self, p):
        """SolutionModifierAux1 ::= empty"""
        # TODO

    def p_production_31(self, p):
        """SolutionModifierAux1 ::= GroupClause"""
        # TODO

    def p_production_32(self, p):
        """SolutionModifierAux2 ::= empty"""
        # TODO

    def p_production_33(self, p):
        """SolutionModifierAux2 ::= HavingClause"""
        # TODO

    def p_production_34(self, p):
        """SolutionModifierAux3 ::= empty"""
        # TODO

    def p_production_35(self, p):
        """SolutionModifierAux3 ::= OrderClause"""
        # TODO

    def p_production_36(self, p):
        """SolutionModifierAux4 ::= empty"""
        # TODO

    def p_production_37(self, p):
        """SolutionModifierAux4 ::= LimitOffsetClauses"""
        # TODO

    def p_production_39(self, p):
        """GroupClause ::= KW_GROUP KW_BY GroupCondition GroupClauseAux"""
        # TODO

    def p_production_40(self, p):
        """GroupClauseAux ::= empty"""
        # TODO

    def p_production_41(self, p):
        """GroupClauseAux ::= GroupCondition GroupClauseAux"""
        # TODO

    def p_production_43(self, p):
        """GroupCondition ::= BuiltInCall"""
        # TODO

    def p_production_44(self, p):
        """GroupCondition ::= SYMB_LP Expression GroupConditionAux SYMB_RP"""
        # TODO

    def p_production_45(self, p):
        """GroupCondition ::= Var"""
        # TODO

    def p_production_46(self, p):
        """GroupConditionAux ::= KW_AS Var"""
        # TODO

    def p_production_47(self, p):
        """GroupConditionAux ::= empty"""
        # TODO

    def p_production_49(self, p):
        """HavingClause ::= KW_HAVING HavingCondition HavingClauseAux"""
        # TODO

    def p_production_50(self, p):
        """HavingClauseAux ::= empty"""
        # TODO

    def p_production_51(self, p):
        """HavingClauseAux ::= HavingClauseAux"""
        # TODO

    def p_production_53(self, p):
        """HavingCondition ::= Constraint"""
        # TODO

    def p_production_55(self, p):
        """OrderClause ::= KW_ORDER KW_BY OrderCondition OrderClauseAux"""
        # TODO

    def p_production_56(self, p):
        """OrderClauseAux ::= empty"""
        # TODO

    def p_production_57(self, p):
        """OrderClauseAux ::= OrderCondition OrderClauseAux"""
        # TODO

    def p_production_59(self, p):
        """OrderCondition ::= Constraint"""
        # TODO

    def p_production_60(self, p):
        """OrderCondition ::= Var"""
        # TODO

    def p_production_61(self, p):
        """OrderCondition ::= OrderConditionAux BrackettedExpression"""
        # TODO

    def p_production_62(self, p):
        """OrderConditionAux ::= KW_ASC"""
        # TODO

    def p_production_63(self, p):
        """OrderConditionAux ::= KW_DESC"""
        # TODO

    def p_production_65(self, p):
        """LimitOffsetClauses ::= LimitClause LimitOffsetClausesAux1"""
        # TODO

    def p_production_66(self, p):
        """LimitOffsetClauses ::= OffsetClause LimitOffsetClausesAux2"""
        # TODO

    def p_production_67(self, p):
        """LimitOffsetClausesAux1 ::= empty"""
        # TODO

    def p_production_68(self, p):
        """LimitOffsetClausesAux1 ::= OffsetClause"""
        # TODO

    def p_production_69(self, p):
        """LimitOffsetClausesAux2 ::= empty"""
        # TODO

    def p_production_70(self, p):
        """LimitOffsetClausesAux2 ::= LimitClause"""
        # TODO

    def p_production_72(self, p):
        """LimitClause ::= KW_LIMIT INTEGER"""
        # TODO

    def p_production_74(self, p):
        """OffsetClause ::= KW_OFFSET INTEGER"""
        # TODO

    def p_production_76(self, p):
        """ValuesClause ::= KW_VALUES DataBlock"""
        # TODO

    def p_production_77(self, p):
        """ValuesClause ::= empty"""
        # TODO

    def p_production_79(self, p):
        """GroupGraphPattern ::= SYMB_LCB GroupGraphPatternSub SYMB_RCB"""
        # TODO

    def p_production_81(self, p):
        """GroupGraphPatternSub ::= GroupGraphPatternSubAux1 GroupGraphPatternSubAux2"""
        # TODO

    def p_production_82(self, p):
        """GroupGraphPatternSubAux1 ::= TriplesBlock"""
        # TODO

    def p_production_83(self, p):
        """GroupGraphPatternSubAux1 ::= empty"""
        # TODO

    def p_production_84(self, p):
        """GroupGraphPatternSubAux2 ::= GraphPatternNotTriples GroupGraphPatternSubAux3 GroupGraphPatternSubAux1 GroupGraphPatternSubAux2"""
        # TODO

    def p_production_85(self, p):
        """GroupGraphPatternSubAux2 ::= empty"""
        # TODO

    def p_production_86(self, p):
        """GroupGraphPatternSubAux3 ::= SYMB_DOT"""
        # TODO

    def p_production_87(self, p):
        """GroupGraphPatternSubAux3 ::= empty"""
        # TODO

    def p_production_89(self, p):
        """TriplesBlock ::= TriplesSameSubjectPath TriplesBlockAux1"""
        # TODO

    def p_production_90(self, p):
        """TriplesBlockAux1 ::= SYMB_DOT TriplesBlockAux2"""
        # TODO

    def p_production_91(self, p):
        """TriplesBlockAux1 ::= empty"""
        # TODO

    def p_production_92(self, p):
        """TriplesBlockAux2 ::= TriplesBlock"""
        # TODO

    def p_production_93(self, p):
        """TriplesBlockAux2 ::= empty"""
        # TODO

    def p_production_95(self, p):
        """GraphPatternNotTriples ::= GroupOrUnionGraphPattern"""
        # TODO

    def p_production_96(self, p):
        """GraphPatternNotTriples ::= OptionalGraphPattern"""
        # TODO

    def p_production_97(self, p):
        """GraphPatternNotTriples ::= MinusGraphPattern"""
        # TODO

    def p_production_98(self, p):
        """GraphPatternNotTriples ::= Filter"""
        # TODO

    def p_production_99(self, p):
        """GraphPatternNotTriples ::= Bind"""
        # TODO

    def p_production_100(self, p):
        """GraphPatternNotTriples ::= InlineData"""
        # TODO

    def p_production_102(self, p):
        """OptionalGraphPattern ::= KW_OPTIONAL GroupGraphPattern"""
        # TODO

    def p_production_104(self, p):
        """Bind ::= KW_BIND SYMB_LP Expression KW_AS Var SYMB_RP"""
        # TODO

    def p_production_106(self, p):
        """InlineData ::= KW_VALUES DataBlock"""
        # TODO

    def p_production_108(self, p):
        """DataBlock ::= InlineDataOneVar"""
        # TODO

    def p_production_109(self, p):
        """DataBlock ::= InlineDataFull"""
        # TODO

    def p_production_111(self, p):
        """InlineDataOneVar ::= Var SYMB_LCB InlineDataOneVarAux SYMB_RCB"""
        # TODO

    def p_production_112(self, p):
        """InlineDataOneVarAux ::= DataBlockValue InlineDataOneVarAux"""
        # TODO

    def p_production_113(self, p):
        """InlineDataOneVarAux ::= empty"""
        # TODO

    def p_production_115(self, p):
        """InlineDataFull ::= InlineDataFullAux1 SYMB_LCB InlineDataFullAux3 SYMB_RCB"""
        # TODO

    def p_production_116(self, p):
        """InlineDataFullAux1 ::= NIL"""
        # TODO

    def p_production_117(self, p):
        """InlineDataFullAux1 ::= SYMB_LP InlineDataFullAux2 SYMB_RP"""
        # TODO

    def p_production_118(self, p):
        """InlineDataFullAux2 ::= Var InlineDataFullAux2"""
        # TODO

    def p_production_119(self, p):
        """InlineDataFullAux2 ::= empty"""
        # TODO

    def p_production_120(self, p):
        """InlineDataFullAux3 ::= InlineDataFullAux4 InlineDataFullAux3"""
        # TODO

    def p_production_121(self, p):
        """InlineDataFullAux3 ::= empty"""
        # TODO

    def p_production_122(self, p):
        """InlineDataFullAux4 ::= SYMB_LP InlineDataFullAux5 SYMB_RP"""
        # TODO

    def p_production_123(self, p):
        """InlineDataFullAux4 ::= NIL"""
        # TODO

    def p_production_124(self, p):
        """InlineDataFullAux5 ::= DataBlockValue InlineDataFullAux5"""
        # TODO

    def p_production_125(self, p):
        """InlineDataFullAux5 ::= empty"""
        # TODO

    def p_production_127(self, p):
        """DataBlockValue ::= iri"""
        # TODO

    def p_production_128(self, p):
        """DataBlockValue ::= RDFLiteral"""
        # TODO

    def p_production_129(self, p):
        """DataBlockValue ::= NumericLiteral"""
        # TODO

    def p_production_130(self, p):
        """DataBlockValue ::= BooleanLiteral"""
        # TODO

    def p_production_131(self, p):
        """DataBlockValue ::= KW_UNDEF"""
        # TODO

    def p_production_133(self, p):
        """MinusGraphPattern ::= KW_MINUS GroupGraphPattern"""
        # TODO

    def p_production_135(self, p):
        """GroupOrUnionGraphPattern ::= GroupGraphPattern GroupOrUnionGraphPatternAux"""
        # TODO

    def p_production_136(self, p):
        """GroupOrUnionGraphPatternAux ::= KW_UNION GroupGraphPattern GroupOrUnionGraphPatternAux"""
        # TODO

    def p_production_137(self, p):
        """GroupOrUnionGraphPatternAux ::= empty"""
        # TODO

    def p_production_139(self, p):
        """Filter ::= KW_FILTER Constraint"""
        # TODO

    def p_production_141(self, p):
        """Constraint ::= BrackettedExpression"""
        # TODO

    def p_production_142(self, p):
        """Constraint ::= BuiltInCall"""
        # TODO

    def p_production_144(self, p):
        """ExpressionList ::= NIL"""
        # TODO

    def p_production_145(self, p):
        """ExpressionList ::= SYMB_LP Expression ExpressionListAux SYMB_RP"""
        # TODO

    def p_production_146(self, p):
        """ExpressionListAux ::= SYMB_COMMA Expression ExpressionListAux"""
        # TODO

    def p_production_147(self, p):
        """ExpressionListAux ::= empty"""
        # TODO

    def p_production_149(self, p):
        """PropertyListNotEmpty ::= Verb ObjectList PropertyListNotEmptyAux2"""
        # TODO

    def p_production_150(self, p):
        """PropertyListNotEmptyAux1 ::= Verb ObjectList"""
        # TODO

    def p_production_151(self, p):
        """PropertyListNotEmptyAux1 ::= empty"""
        # TODO

    def p_production_152(self, p):
        """PropertyListNotEmptyAux2 ::= SYMB_SEMICOLON PropertyListNotEmptyAux1 PropertyListNotEmptyAux2"""
        # TODO

    def p_production_153(self, p):
        """PropertyListNotEmptyAux2 ::= empty"""
        # TODO

    def p_production_155(self, p):
        """Verb ::= VarOrIri"""
        # TODO

    def p_production_156(self, p):
        """Verb ::= SYMB_a"""
        # TODO

    def p_production_158(self, p):
        """ObjectList ::= Object ObjectListAux"""
        # TODO

    def p_production_159(self, p):
        """ObjectListAux ::= SYMB_COMMA Object ObjectListAux"""
        # TODO

    def p_production_160(self, p):
        """ObjectListAux ::= empty"""
        # TODO

    def p_production_162(self, p):
        """Object ::= GraphNode"""
        # TODO

    def p_production_164(self, p):
        """TriplesSameSubjectPath ::= VarOrTerm PropertyListPathNotEmpty"""
        # TODO

    def p_production_165(self, p):
        """TriplesSameSubjectPath ::= TriplesNodePath PropertyListPath"""
        # TODO

    def p_production_167(self, p):
        """PropertyListPath ::= PropertyListPathNotEmpty"""
        # TODO

    def p_production_168(self, p):
        """PropertyListPath ::= empty"""
        # TODO

    def p_production_170(self, p):
        """PropertyListPathNotEmpty ::= PropertyListPathNotEmptyAux1 ObjectListPath PropertyListPathNotEmptyAux2"""
        # TODO

    def p_production_171(self, p):
        """PropertyListPathNotEmptyAux1 ::= VerbPath"""
        # TODO

    def p_production_172(self, p):
        """PropertyListPathNotEmptyAux1 ::= VerbSimple"""
        # TODO

    def p_production_173(self, p):
        """PropertyListPathNotEmptyAux2 ::= SYMB_SEMICOLON PropertyListPathNotEmptyAux3"""
        # TODO

    def p_production_174(self, p):
        """PropertyListPathNotEmptyAux2 ::= empty"""
        # TODO

    def p_production_175(self, p):
        """PropertyListPathNotEmptyAux3 ::= PropertyListPathNotEmptyAux1 ObjectList"""
        # TODO

    def p_production_176(self, p):
        """PropertyListPathNotEmptyAux3 ::= empty"""
        # TODO

    def p_production_178(self, p):
        """VerbPath ::= Path"""
        # TODO

    def p_production_180(self, p):
        """VerbSimple ::= Var"""
        # TODO

    def p_production_182(self, p):
        """ObjectListPath ::= ObjectPath ObjectListPathAux"""
        # TODO

    def p_production_183(self, p):
        """ObjectListPathAux ::= SYMB_COMMA ObjectPath"""
        # TODO

    def p_production_184(self, p):
        """ObjectListPathAux ::= empty"""
        # TODO

    def p_production_186(self, p):
        """ObjectPath ::= GraphNodePath"""
        # TODO

    def p_production_188(self, p):
        """Path ::= PathAlternative"""
        # TODO

    def p_production_190(self, p):
        """PathAlternative ::= PathSequence PathAlternativeAux"""
        # TODO

    def p_production_191(self, p):
        """PathAlternativeAux ::= SYMB_PIPE PathSequence PathAlternativeAux"""
        # TODO

    def p_production_192(self, p):
        """PathAlternativeAux ::= empty"""
        # TODO

    def p_production_194(self, p):
        """PathSequence ::= PathEltOrInverse PathSequenceAux"""
        # TODO

    def p_production_195(self, p):
        """PathSequenceAux ::= SYMB_SLASH PathEltOrInverse PathSequenceAux"""
        # TODO

    def p_production_196(self, p):
        """PathSequenceAux ::= empty"""
        # TODO

    def p_production_198(self, p):
        """PathElt ::= PathPrimary PathEltAux"""
        # TODO

    def p_production_199(self, p):
        """PathEltAux ::= PathMod"""
        # TODO

    def p_production_200(self, p):
        """PathEltAux ::= empty"""
        # TODO

    def p_production_202(self, p):
        """PathEltOrInverse ::= PathElt"""
        # TODO

    def p_production_203(self, p):
        """PathEltOrInverse ::= SYMB_CIRCUMFLEX PathElt"""
        # TODO

    def p_production_205(self, p):
        """PathMod ::= SYMB_QUESTION"""
        # TODO

    def p_production_206(self, p):
        """PathMod ::= SYMB_ASTERISK"""
        # TODO

    def p_production_207(self, p):
        """PathMod ::= SYMB_PLUS"""
        # TODO

    def p_production_209(self, p):
        """PathPrimary ::= iri"""
        # TODO

    def p_production_210(self, p):
        """PathPrimary ::= SYMB_a"""
        # TODO

    def p_production_211(self, p):
        """PathPrimary ::= SYMB_EXCLAMATION PathNegatedPropertySet"""
        # TODO

    def p_production_212(self, p):
        """PathPrimary ::= SYMB_LP Path SYMB_RP"""
        # TODO

    def p_production_215(self, p):
        """PathNegatedPropertySet ::= PathOneInPropertySet"""
        # TODO

    def p_production_216(self, p):
        """PathNegatedPropertySet ::= SYMB_LP PathNegatedPropertySetAux1 SYMB_RP"""
        # TODO

    def p_production_217(self, p):
        """PathNegatedPropertySetAux1 ::= PathOneInPropertySet PathNegatedPropertySetAux2"""
        # TODO

    def p_production_218(self, p):
        """PathNegatedPropertySetAux1 ::= empty"""
        # TODO

    def p_production_219(self, p):
        """PathNegatedPropertySetAux2 ::= SYMB_PIPE PathOneInPropertySet PathNegatedPropertySetAux2"""
        # TODO

    def p_production_220(self, p):
        """PathNegatedPropertySetAux2 ::= empty"""
        # TODO

    def p_production_222(self, p):
        """PathOneInPropertySet ::= iri"""
        # TODO

    def p_production_223(self, p):
        """PathOneInPropertySet ::= SYMB_a"""
        # TODO

    def p_production_224(self, p):
        """PathOneInPropertySet ::= SYMB_CIRCUMFLEX PathOneInPropertySetAux"""
        # TODO

    def p_production_225(self, p):
        """PathOneInPropertySetAux ::= iri"""
        # TODO

    def p_production_226(self, p):
        """PathOneInPropertySetAux ::= SYMB_a"""
        # TODO

    def p_production_228(self, p):
        """TriplesNode ::= Collection"""
        # TODO

    def p_production_229(self, p):
        """TriplesNode ::= BlankNodePropertyList"""
        # TODO

    def p_production_231(self, p):
        """BlankNodePropertyList ::= SYMB_LSB PropertyListNotEmpty SYMB_RSB"""
        # TODO

    def p_production_233(self, p):
        """TriplesNodePath ::= CollectionPath"""
        # TODO

    def p_production_234(self, p):
        """TriplesNodePath ::= BlankNodePropertyListPath"""
        # TODO

    def p_production_236(self, p):
        """BlankNodePropertyListPath ::= SYMB_LSB PropertyListPathNotEmpty SYMB_RSB"""
        # TODO

    def p_production_238(self, p):
        """Collection ::= SYMB_LP GraphNode CollectionAux SYMB_RP"""
        # TODO

    def p_production_239(self, p):
        """CollectionAux ::= GraphNode CollectionAux"""
        # TODO

    def p_production_240(self, p):
        """CollectionAux ::= empty"""
        # TODO

    def p_production_242(self, p):
        """CollectionPath ::= SYMB_LP GraphNodePath CollectionPathAux SYMB_RP"""
        # TODO

    def p_production_243(self, p):
        """CollectionPathAux ::= GraphNodePath CollectionPathAux"""
        # TODO

    def p_production_244(self, p):
        """CollectionPathAux ::= empty"""
        # TODO

    def p_production_246(self, p):
        """GraphNode ::= TriplesNode"""
        # TODO

    def p_production_247(self, p):
        """GraphNode ::= VarOrTerm"""
        # TODO

    def p_production_249(self, p):
        """GraphNodePath ::= VarOrTerm"""
        # TODO

    def p_production_250(self, p):
        """GraphNodePath ::= TriplesNodePath"""
        # TODO

    def p_production_252(self, p):
        """VarOrTerm ::= Var"""
        # TODO

    def p_production_253(self, p):
        """VarOrTerm ::= GraphTerm"""
        # TODO

    def p_production_255(self, p):
        """VarOrIri ::= Var"""
        # TODO

    def p_production_256(self, p):
        """VarOrIri ::= iri"""
        # TODO

    def p_production_258(self, p):
        """Var ::= VAR1"""
        # TODO

    def p_production_259(self, p):
        """Var ::= VAR2"""
        # TODO

    def p_production_261(self, p):
        """GraphTerm ::= iri"""
        # TODO

    def p_production_262(self, p):
        """GraphTerm ::= RDFLiteral"""
        # TODO

    def p_production_263(self, p):
        """GraphTerm ::= NumericLiteral"""
        # TODO

    def p_production_264(self, p):
        """GraphTerm ::= BooleanLiteral"""
        # TODO

    def p_production_265(self, p):
        """GraphTerm ::= BlankNode"""
        # TODO

    def p_production_266(self, p):
        """GraphTerm ::= NIL"""
        # TODO

    def p_production_268(self, p):
        """Expression ::= ConditionalOrExpression"""
        # TODO

    def p_production_270(self, p):
        """ConditionalOrExpression ::= ConditionalAndExpression ConditionalOrExpressionAux"""
        # TODO

    def p_production_271(self, p):
        """ConditionalOrExpressionAux ::= SYMB_OR ConditionalAndExpression ConditionalOrExpressionAux"""
        # TODO

    def p_production_272(self, p):
        """ConditionalOrExpressionAux ::= empty"""
        # TODO

    def p_production_274(self, p):
        """ConditionalAndExpression ::= ValueLogical ConditionalAndExpressionAux"""
        # TODO

    def p_production_275(self, p):
        """ConditionalAndExpressionAux ::= SYMB_AND ValueLogical ConditionalAndExpressionAux"""
        # TODO

    def p_production_276(self, p):
        """ConditionalAndExpressionAux ::= empty"""
        # TODO

    def p_production_278(self, p):
        """ValueLogical ::= RelationalExpression"""
        # TODO

    def p_production_280(self, p):
        """RelationalExpression ::= NumericExpression"""
        # TODO

    def p_production_281(self, p):
        """RelationalExpressionAux ::= SYMB_EQ NumericExpression"""
        # TODO

    def p_production_282(self, p):
        """RelationalExpressionAux ::= SYMB_NEQ NumericExpression"""
        # TODO

    def p_production_283(self, p):
        """RelationalExpressionAux ::= SYMB_LT NumericExpression"""
        # TODO

    def p_production_284(self, p):
        """RelationalExpressionAux ::= SYMB_GT NumericExpression"""
        # TODO

    def p_production_285(self, p):
        """RelationalExpressionAux ::= SYMB_LTE NumericExpression"""
        # TODO

    def p_production_286(self, p):
        """RelationalExpressionAux ::= SYMB_GTE NumericExpression"""
        # TODO

    def p_production_287(self, p):
        """RelationalExpressionAux ::= KW_IN ExpressionList"""
        # TODO

    def p_production_288(self, p):
        """RelationalExpressionAux ::= KW_NOT KW_IN ExpressionList"""
        # TODO

    def p_production_289(self, p):
        """RelationalExpressionAux ::= empty"""
        # TODO

    def p_production_291(self, p):
        """NumericExpression ::= AdditiveExpression"""
        # TODO

    def p_production_293(self, p):
        """AdditiveExpression ::= MultiplicativeExpression"""
        # TODO

    def p_production_294(self, p):
        """AdditiveExpressionAux1 ::= AdditiveExpressionAux2 AdditiveExpressionAux1"""
        # TODO

    def p_production_295(self, p):
        """AdditiveExpressionAux1 ::= empty"""
        # TODO

    def p_production_296(self, p):
        """AdditiveExpressionAux2 ::= SYMB_PLUS MultiplicativeExpression"""
        # TODO

    def p_production_297(self, p):
        """AdditiveExpressionAux2 ::= SYMB_MINUS MultiplicativeExpression"""
        # TODO

    def p_production_298(self, p):
        """AdditiveExpressionAux2 ::= AdditiveExpressionAux3 AdditiveExpressionAux4"""
        # TODO

    def p_production_299(self, p):
        """AdditiveExpressionAux3 ::= NumericLiteralPositive"""
        # TODO

    def p_production_300(self, p):
        """AdditiveExpressionAux3 ::= NumericLiteralNegative"""
        # TODO

    def p_production_301(self, p):
        """AdditiveExpressionAux4 ::= SYMB_ASTERISK UnaryExpression AdditiveExpressionAux4"""
        # TODO

    def p_production_302(self, p):
        """AdditiveExpressionAux4 ::= SYMB_SLASH UnaryExpression AdditiveExpressionAux4"""
        # TODO

    def p_production_304(self, p):
        """MultiplicativeExpression ::= UnaryExpression MultiplicativeExpressionAux"""
        # TODO

    def p_production_305(self, p):
        """MultiplicativeExpressionAux ::= SYMB_ASTERISK UnaryExpression MultiplicativeExpressionAux"""
        # TODO

    def p_production_306(self, p):
        """MultiplicativeExpressionAux ::= SYMB_SLASH UnaryExpression MultiplicativeExpressionAux"""
        # TODO

    def p_production_307(self, p):
        """MultiplicativeExpressionAux ::= empty"""
        # TODO

    def p_production_309(self, p):
        """UnaryExpression ::= SYMB_EXCLAMATION PrimaryExpression"""
        # TODO

    def p_production_310(self, p):
        """UnaryExpression ::= SYMB_PLUS PrimaryExpression"""
        # TODO

    def p_production_311(self, p):
        """UnaryExpression ::= SYMB_MINUS PrimaryExpression"""
        # TODO

    def p_production_312(self, p):
        """UnaryExpression ::= PrimaryExpression"""
        # TODO

    def p_production_314(self, p):
        """PrimaryExpression ::= BrackettedExpression"""
        # TODO

    def p_production_315(self, p):
        """PrimaryExpression ::= BuiltInCall"""
        # TODO

    def p_production_316(self, p):
        """PrimaryExpression ::= iri"""
        # TODO

    def p_production_317(self, p):
        """PrimaryExpression ::= RDFLiteral"""
        # TODO

    def p_production_318(self, p):
        """PrimaryExpression ::= NumericLiteral"""
        # TODO

    def p_production_319(self, p):
        """PrimaryExpression ::= BooleanLiteral"""
        # TODO

    def p_production_320(self, p):
        """PrimaryExpression ::= Var"""
        # TODO

    def p_production_322(self, p):
        """BrackettedExpression ::= SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_324(self, p):
        """BuiltInCall ::= Aggregate"""
        # TODO

    def p_production_325(self, p):
        """BuiltInCall ::= FUNC_RAND NIL"""
        # TODO

    def p_production_326(self, p):
        """BuiltInCall ::= FUNC_ABS SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_327(self, p):
        """BuiltInCall ::= FUNC_CEIL SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_328(self, p):
        """BuiltInCall ::= FUNC_FLOOR SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_329(self, p):
        """BuiltInCall ::= FUNC_ROUND SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_330(self, p):
        """BuiltInCall ::= FUNC_CONCAT ExpressionList"""
        # TODO

    def p_production_331(self, p):
        """BuiltInCall ::= SubstringExpression"""
        # TODO

    def p_production_332(self, p):
        """BuiltInCall ::= FUNC_STRLEN SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_333(self, p):
        """BuiltInCall ::= StrReplaceExpression"""
        # TODO

    def p_production_334(self, p):
        """BuiltInCall ::= FUNC_UCASE SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_335(self, p):
        """BuiltInCall ::= FUNC_LCASE SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_336(self, p):
        """BuiltInCall ::= FUNC_CONTAINS SYMB_LP Expression SYMB_COMMA Expression SYMB_RP"""
        # TODO

    def p_production_337(self, p):
        """BuiltInCall ::= FUNC_STRSTARTS SYMB_LP Expression SYMB_COMMA Expression SYMB_RP"""
        # TODO

    def p_production_338(self, p):
        """BuiltInCall ::= FUNC_STRENDS SYMB_LP Expression SYMB_COMMA Expression SYMB_RP"""
        # TODO

    def p_production_339(self, p):
        """BuiltInCall ::= FUNC_YEAR SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_340(self, p):
        """BuiltInCall ::= FUNC_MONTH SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_341(self, p):
        """BuiltInCall ::= FUNC_DAY SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_342(self, p):
        """BuiltInCall ::= FUNC_HOURS SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_343(self, p):
        """BuiltInCall ::= FUNC_MINUTES SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_344(self, p):
        """BuiltInCall ::= FUNC_SECONDS SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_345(self, p):
        """BuiltInCall ::= FUNC_TIMEZONE SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_346(self, p):
        """BuiltInCall ::= FUNC_TZ SYMB_LP Expression SYMB_RP"""
        # TODO

    def p_production_347(self, p):
        """BuiltInCall ::= FUNC_NOW NIL"""
        # TODO

    def p_production_348(self, p):
        """BuiltInCall ::= FUNC_COALESCE ExpressionList"""
        # TODO

    def p_production_349(self, p):
        """BuiltInCall ::= RegexExpression"""
        # TODO

    def p_production_351(self, p):
        """RegexExpression ::= FUNC_REGEX SYMB_LP Expression SYMB_COMMA Expression RegexExpressionAux SYMB_RP"""
        # TODO

    def p_production_352(self, p):
        """RegexExpressionAux ::= SYMB_COMMA Expression"""
        # TODO

    def p_production_353(self, p):
        """RegexExpressionAux ::= empty"""
        # TODO

    def p_production_355(self, p):
        """SubstringExpression ::= FUNC_SUBSTR SYMB_LP Expression SYMB_COMMA Expression SubstringExpressionAux SYMB_RP"""
        # TODO

    def p_production_356(self, p):
        """SubstringExpressionAux ::= SYMB_COMMA Expression"""
        # TODO

    def p_production_357(self, p):
        """SubstringExpressionAux ::= empty"""
        # TODO

    def p_production_359(self, p):
        """StrReplaceExpression ::= FUNC_REPLACE SYMB_LP Expression SYMB_COMMA Expression SYMB_COMMA Expression StrReplaceExpressionAux SYMB_RP"""
        # TODO

    def p_production_360(self, p):
        """StrReplaceExpressionAux ::= SYMB_COMMA Expression"""
        # TODO

    def p_production_361(self, p):
        """StrReplaceExpressionAux ::= empty"""
        # TODO

    def p_production_363(self, p):
        """Aggregate ::= FUNC_COUNT SYMB_LP AggregateAux1 AggregateAux2 SYMB_RP"""
        # TODO

    def p_production_364(self, p):
        """Aggregate ::= FUNC_SUM SYMB_LP AggregateAux1 Expression SYMB_RP"""
        # TODO

    def p_production_365(self, p):
        """Aggregate ::= FUNC_MIN SYMB_LP AggregateAux1 Expression SYMB_RP"""
        # TODO

    def p_production_366(self, p):
        """Aggregate ::= FUNC_MAX SYMB_LP AggregateAux1 Expression SYMB_RP"""
        # TODO

    def p_production_367(self, p):
        """Aggregate ::= FUNC_AVG SYMB_LP AggregateAux1 Expression SYMB_RP"""
        # TODO

    def p_production_368(self, p):
        """AggregateAux1 ::= KW_DISTINCT"""
        # TODO

    def p_production_369(self, p):
        """AggregateAux1 ::= empty"""
        # TODO

    def p_production_370(self, p):
        """AggregateAux2 ::= SYMB_ASTERISK"""
        # TODO

    def p_production_371(self, p):
        """AggregateAux2 ::= Expression"""
        # TODO

    def p_production_373(self, p):
        """RDFLiteral ::= String RDFLiteralAux1"""
        # TODO

    def p_production_374(self, p):
        """RDFLiteralAux1 ::= LANGTAG"""
        # TODO

    def p_production_375(self, p):
        """RDFLiteralAux1 ::= SYMB_C2 iri"""
        # TODO

    def p_production_376(self, p):
        """RDFLiteralAux1 ::= empty"""
        # TODO

    def p_production_378(self, p):
        """NumericLiteral ::= NumericLiteralUnsigned"""
        # TODO

    def p_production_379(self, p):
        """NumericLiteral ::= NumericLiteralPositive"""
        # TODO

    def p_production_380(self, p):
        """NumericLiteral ::= NumericLiteralNegative"""
        # TODO

    def p_production_382(self, p):
        """NumericLiteralUnsigned ::= INTEGER"""
        # TODO

    def p_production_383(self, p):
        """NumericLiteralUnsigned ::= DECIMAL"""
        # TODO

    def p_production_384(self, p):
        """NumericLiteralUnsigned ::= DOUBLE"""
        # TODO

    def p_production_386(self, p):
        """NumericLiteralPositive ::= INTEGER_POSITIVE"""
        # TODO

    def p_production_387(self, p):
        """NumericLiteralPositive ::= DECIMAL_POSITIVE"""
        # TODO

    def p_production_388(self, p):
        """NumericLiteralPositive ::= DOUBLE_POSITIVE"""
        # TODO

    def p_production_390(self, p):
        """NumericLiteralNegative ::= INTEGER_NEGATIVE"""
        # TODO

    def p_production_391(self, p):
        """NumericLiteralNegative ::= DECIMAL_NEGATIVE"""
        # TODO

    def p_production_392(self, p):
        """NumericLiteralNegative ::= DOUBLE_NEGATIVE"""
        # TODO

    def p_production_394(self, p):
        """BooleanLiteral ::= SYMB_TRUE"""
        # TODO

    def p_production_395(self, p):
        """BooleanLiteral ::= SYMB_FALSE"""
        # TODO

    def p_production_397(self, p):
        """String ::= STRING_LITERAL1"""
        # TODO

    def p_production_398(self, p):
        """String ::= STRING_LITERAL2"""
        # TODO

    def p_production_399(self, p):
        """String ::= STRING_LITERAL_LONG1"""
        # TODO

    def p_production_400(self, p):
        """String ::= STRING_LITERAL_LONG2"""
        # TODO

    def p_production_402(self, p):
        """iri ::= IRIREF"""
        # TODO

    def p_production_403(self, p):
        """iri ::= PrefixedName"""
        # TODO

    def p_production_405(self, p):
        """PrefixedName ::= PNAME_LN"""
        # TODO

    def p_production_406(self, p):
        """PrefixedName ::= PNAME_NS"""
        # TODO

    def p_production_408(self, p):
        """BlankNode ::= BLANK_NODE_LABEL"""
        # TODO

    def p_production_409(self, p):
        """BlankNode ::= ANON"""
        # TODO

    def p_empty(self, p):
        """empty :"""
        pass

    def p_error(self, p):
        print('ERROR!')
        print(p)
