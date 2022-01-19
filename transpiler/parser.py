from typing import List, Union

from ply import yacc

from .lexer import SelectSparqlLexer
from .structures import nodes
from .structures.query import Query


class SelectSparqlParser:
    def __init__(self, **kwargs):
        self.lexer = SelectSparqlLexer()
        self.tokens = self.lexer.tokens

        self.yacc = yacc.yacc(module=self,
                              check_recursion=False,
                              **kwargs)

        self.query = Query()
        self.selecteds: Union[List[str], str] = []

    def parse(self, source_code: str) -> str:
        return self.yacc.parse(source_code, lexer=self.lexer)

    def p_production_0(self, p):
        """QueryUnit : Query"""
        # Mark selected variables
        if self.selecteds == "*":
            is_selected = lambda *args: True
        else:
            def is_selected(name): return name in self.selecteds

        for var in self.query.variables:
            if is_selected(var.name):
                var.selected = True

        p[0] = self.query

    def p_production_2(self, p):
        """Query : Prologue SelectQuery"""
        pass

    def p_production_4(self, p):
        """Prologue : BaseDecl Prologue"""
        pass

    def p_production_5(self, p):
        """Prologue : PrefixDecl Prologue"""
        # TODO
        raise NotImplementedError

    def p_production_6(self, p):
        """Prologue : empty"""
        pass

    def p_production_8(self, p):
        """BaseDecl : KW_BASE IRIREF"""
        # TODO
        raise NotImplementedError

    def p_production_11(self, p):
        """PrefixDecl : KW_PREFIX PNAME_NS IRIREF"""
        # TODO
        raise NotImplementedError

    def p_production_13(self, p):
        """SelectQuery : SelectClause WhereClause SolutionModifier"""
        pass

    def p_production_15(self, p):
        """SelectClause : KW_SELECT SelectClauseAux1"""
        pass

    def p_production_16(self, p):
        """SelectClauseAux1 : SelectClauseAux2"""
        pass

    def p_production_17(self, p):
        """SelectClauseAux1 : KW_DISTINCT SelectClauseAux2"""
        # TODO
        raise NotImplementedError

    def p_production_18(self, p):
        """SelectClauseAux1 : KW_REDUCED SelectClauseAux2"""
        # TODO
        raise NotImplementedError

    def p_production_19(self, p):
        """SelectClauseAux2 : SYMB_ASTERISK"""
        self.selecteds = "*"

    def p_production_20(self, p):
        """SelectClauseAux2 : Var SelectClauseAux3"""
        self.selecteds.append(p[1].name)

    def p_production_21(self, p):
        """SelectClauseAux2 : SYMB_LP Expression KW_AS Var SYMB_RP SelectClauseAux3"""
        self.selecteds.append(p[4].name)

    def p_production_22(self, p):
        """SelectClauseAux3 : Var SelectClauseAux3"""
        self.selecteds.append(p[1].name)

    def p_production_23(self, p):
        """SelectClauseAux3 : SYMB_LP Expression KW_AS Var SYMB_RP SelectClauseAux3"""
        self.selecteds.append(p[4].name)

    def p_production_24(self, p):
        """SelectClauseAux3 : empty"""
        pass

    def p_production_26(self, p):
        """WhereClause : GroupGraphPattern"""
        self.query.mandatory = p[1]

    def p_production_27(self, p):
        """WhereClause : KW_WHERE GroupGraphPattern"""
        self.query.mandatory = p[2]

    def p_production_29(self, p):
        """SolutionModifier : SolutionModifierAux1 SolutionModifierAux2 SolutionModifierAux3 SolutionModifierAux4"""
        pass

    def p_production_30(self, p):
        """SolutionModifierAux1 : empty"""
        pass

    def p_production_31(self, p):
        """SolutionModifierAux1 : GroupClause"""
        pass

    def p_production_32(self, p):
        """SolutionModifierAux2 : empty"""
        pass

    def p_production_33(self, p):
        """SolutionModifierAux2 : HavingClause"""
        pass

    def p_production_34(self, p):
        """SolutionModifierAux3 : empty"""
        pass

    def p_production_35(self, p):
        """SolutionModifierAux3 : OrderClause"""
        pass

    def p_production_36(self, p):
        """SolutionModifierAux4 : empty"""
        pass

    def p_production_37(self, p):
        """SolutionModifierAux4 : LimitOffsetClauses"""
        pass

    def p_production_39(self, p):
        """GroupClause : KW_GROUP KW_BY GroupCondition GroupClauseAux"""
        conds = p[4]
        conds.append(p[3])
        self.query.modifiers.group = nodes.GroupClauseNode(conds)

    def p_production_40(self, p):
        """GroupClauseAux : empty"""
        p[0] = []

    def p_production_41(self, p):
        """GroupClauseAux : GroupCondition GroupClauseAux"""
        conds = p[2]
        conds.append(p[1])
        p[0] = conds

    def p_production_43(self, p):
        """GroupCondition : BuiltInCall"""
        p[0] = nodes.GroupCondition(value=p[1])

    def p_production_44(self, p):
        """GroupCondition : SYMB_LP Expression GroupConditionAux SYMB_RP"""
        p[0] = nodes.GroupCondition(value=p[2], alias=p[3])

    def p_production_45(self, p):
        """GroupCondition : Var"""
        p[0] = nodes.GroupCondition(value=p[1])

    def p_production_46(self, p):
        """GroupConditionAux : KW_AS Var"""
        p[0] = p[2]

    def p_production_47(self, p):
        """GroupConditionAux : empty"""
        p[0] = None

    def p_production_49(self, p):
        """HavingClause : KW_HAVING HavingCondition HavingClauseAux"""
        conds = p[3]
        conds.append(p[2])
        self.query.modifiers.having = nodes.HavingClauseNode(conds)

    def p_production_50(self, p):
        """HavingClauseAux : empty"""
        p[0] = []

    def p_production_51(self, p):
        """HavingClauseAux : HavingCondition HavingClauseAux"""
        conds = p[2]
        conds.append(p[1])
        p[0] = conds

    def p_production_53(self, p):
        """HavingCondition : Constraint"""
        p[0] = p[1]

    def p_production_55(self, p):
        """OrderClause : KW_ORDER KW_BY OrderCondition OrderClauseAux"""
        conds = p[4]
        conds.append(p[3])
        self.query.modifiers.order = nodes.OrderClauseNode(conds)

    def p_production_56(self, p):
        """OrderClauseAux : empty"""
        p[0] = []

    def p_production_57(self, p):
        """OrderClauseAux : OrderCondition OrderClauseAux"""
        conds = p[2]
        conds.append(p[1])
        p[0] = conds

    def p_production_59(self, p):
        """OrderCondition : Constraint"""
        p[0] = nodes.OrderCondition(exp=p[1])

    def p_production_60(self, p):
        """OrderCondition : Var"""
        p[0] = nodes.OrderCondition(var=p[1])

    def p_production_61(self, p):
        """OrderCondition : OrderConditionAux BrackettedExpression"""
        p[0] = nodes.OrderCondition(order=p[1], exp=p[2])

    def p_production_62(self, p):
        """OrderConditionAux : KW_ASC"""
        p[0] = p[1]

    def p_production_63(self, p):
        """OrderConditionAux : KW_DESC"""
        p[0] = p[1]

    def p_production_65(self, p):
        """LimitOffsetClauses : LimitClause LimitOffsetClausesAux1"""
        pass

    def p_production_66(self, p):
        """LimitOffsetClauses : OffsetClause LimitOffsetClausesAux2"""
        pass

    def p_production_67(self, p):
        """LimitOffsetClausesAux1 : empty"""
        pass

    def p_production_68(self, p):
        """LimitOffsetClausesAux1 : OffsetClause"""
        pass

    def p_production_69(self, p):
        """LimitOffsetClausesAux2 : empty"""
        pass

    def p_production_70(self, p):
        """LimitOffsetClausesAux2 : LimitClause"""
        pass

    def p_production_72(self, p):
        """LimitClause : KW_LIMIT INTEGER"""
        self.query.modifiers.limit = p[2]

    def p_production_74(self, p):
        """OffsetClause : KW_OFFSET INTEGER"""
        self.query.modifiers.offset = p[2]

    def p_production_79(self, p):
        """GroupGraphPattern : SYMB_LCB GroupGraphPatternSub SYMB_RCB"""
        p[0] = p[2]

    def p_production_81(self, p):
        """GroupGraphPatternSub : GroupGraphPatternSubAux1 GroupGraphPatternSubAux2"""
        and_triples = p[1]
        or_block = None

        if p[2] is not None:
            if p[2]['and_block'] is not None:
                and_triples.extend(p[2]['and_block'])

            if p[2]['or_block'] is not None:
                or_block = p[2]['or_block']

        p[0] = nodes.GraphPattern(and_triples, or_block)

    def p_production_82(self, p):
        """GroupGraphPatternSubAux1 : TriplesBlock"""
        p[0] = p[1]

    def p_production_83(self, p):
        """GroupGraphPatternSubAux1 : empty"""
        p[0] = []

    def p_production_84(self, p):
        """GroupGraphPatternSubAux2 : GraphPatternNotTriples GroupGraphPatternSubAux3 GroupGraphPatternSubAux1 GroupGraphPatternSubAux2"""
        data = {
            'and_block': p[3],
            'or_block': p[1]
        }
        p[0] = data

    def p_production_85(self, p):
        """GroupGraphPatternSubAux2 : empty"""
        pass

    def p_production_86(self, p):
        """GroupGraphPatternSubAux3 : SYMB_DOT"""
        pass

    def p_production_87(self, p):
        """GroupGraphPatternSubAux3 : empty"""
        pass

    def p_production_89(self, p):
        """TriplesBlock : TriplesSameSubjectPath TriplesBlockAux1"""
        triples = p[1]
        if p[2] is not None:
            triples.extend(p[2])

        p[0] = triples

    def p_production_90(self, p):
        """TriplesBlockAux1 : SYMB_DOT TriplesBlockAux2"""
        p[0] = p[2]

    def p_production_91(self, p):
        """TriplesBlockAux1 : empty"""
        p[0] = []

    def p_production_92(self, p):
        """TriplesBlockAux2 : TriplesBlock"""
        p[0] = p[1]

    def p_production_93(self, p):
        """TriplesBlockAux2 : empty"""
        p[0] = []

    def p_production_95(self, p):
        """GraphPatternNotTriples : GroupOrUnionGraphPattern"""
        p[0] = p[1]

    def p_production_96(self, p):
        """GraphPatternNotTriples : OptionalGraphPattern"""
        pass

    def p_production_97(self, p):
        """GraphPatternNotTriples : MinusGraphPattern"""
        pass

    def p_production_98(self, p):
        """GraphPatternNotTriples : Filter"""
        pass

    def p_production_102(self, p):
        """OptionalGraphPattern : KW_OPTIONAL GroupGraphPattern"""
        self.query.optional = structures.OptionalNode(p[2])

    def p_production_133(self, p):
        """MinusGraphPattern : KW_MINUS GroupGraphPattern"""
        self.query.minus = structures.MinusNode(p[2])

    def p_production_135(self, p):
        """GroupOrUnionGraphPattern : GroupGraphPattern GroupOrUnionGraphPatternAux"""
        patterns = p[2]
        patterns.append(p[1])

        p[0] = patterns

    def p_production_136(self, p):
        """GroupOrUnionGraphPatternAux : KW_UNION GroupGraphPattern GroupOrUnionGraphPatternAux"""
        patterns = p[3]
        patterns.append(p[2])
        p[0] = patterns

    def p_production_137(self, p):
        """GroupOrUnionGraphPatternAux : empty"""
        p[0] = []

    def p_production_139(self, p):
        """Filter : KW_FILTER Constraint"""
        self.query.filter = nodes.FilterNode(p[2])

    def p_production_141(self, p):
        """Constraint : BrackettedExpression"""
        p[0] = p[1]

    def p_production_142(self, p):
        """Constraint : BuiltInCall"""
        p[0] = p[1]

    def p_production_144(self, p):
        """ExpressionList : NIL"""
        p[0] = []

    def p_production_145(self, p):
        """ExpressionList : SYMB_LP Expression ExpressionListAux SYMB_RP"""
        exps = p[2]
        exps.extend(p[3])
        p[0] = exps

    def p_production_146(self, p):
        """ExpressionListAux : SYMB_COMMA Expression ExpressionListAux"""
        exps = p[2]
        exps.extend(p[3])
        p[0] = exps

    def p_production_147(self, p):
        """ExpressionListAux : empty"""
        p[0] = []

    def p_production_149(self, p):
        """PropertyListNotEmpty : Verb ObjectList PropertyListNotEmptyAux2"""
        props = [(p[1], p[2])]
        props.extend(p[3])

        p[0] = props

    def p_production_150(self, p):
        """PropertyListNotEmptyAux1 : Verb ObjectList"""
        p[0] = (p[1], p[2])

    def p_production_151(self, p):
        """PropertyListNotEmptyAux1 : empty"""
        p[0] = None

    def p_production_152(self, p):
        """PropertyListNotEmptyAux2 : SYMB_SEMICOLON PropertyListNotEmptyAux1 PropertyListNotEmptyAux2"""
        props = p[3]

        if p[3] is not None:
            props.append(p[2])

        p[0] = props

    def p_production_153(self, p):
        """PropertyListNotEmptyAux2 : empty"""
        p[0] = []

    def p_production_155(self, p):
        """Verb : VarOrIri"""
        p[0] = p[1]

    def p_production_156(self, p):
        """Verb : SYMB_a"""
        p[0] = "rdf:type"

    def p_production_158(self, p):
        """ObjectList : Object ObjectListAux"""
        obj_list = p[2]
        obj_list.append(p[1])

        p[0] = obj_list

    def p_production_159(self, p):
        """ObjectListAux : SYMB_COMMA Object ObjectListAux"""
        obj_list = p[3]
        obj_list.append(p[2])

        p[0] = obj_list

    def p_production_160(self, p):
        """ObjectListAux : empty"""
        p[0] = []

    def p_production_162(self, p):
        """Object : GraphNode"""
        if isinstance(p[1], str):
            p[0] = p[1]

        else:
            raise NotImplementedError

    def p_production_164(self, p):
        """TriplesSameSubjectPath : VarOrTerm PropertyListPathNotEmpty"""
        triples = []
        for prop, obj in p[2]:
            triples.append(nodes.Triple(p[1], prop, obj))

        p[0] = triples

    def p_production_165(self, p):
        """TriplesSameSubjectPath : TriplesNodePath PropertyListPath"""
        # TODO
        raise NotImplementedError

    def p_production_167(self, p):
        """PropertyListPath : PropertyListPathNotEmpty"""
        # TODO
        raise NotImplementedError

    def p_production_168(self, p):
        """PropertyListPath : empty"""
        # TODO
        raise NotImplementedError

    def p_production_170(self, p):
        """PropertyListPathNotEmpty : PropertyListPathNotEmptyAux1 ObjectListPath PropertyListPathNotEmptyAux2"""
        p[0] = p[3]
        for obj in p[2]:
            p[0].append((p[1], obj))

    def p_production_171(self, p):
        """PropertyListPathNotEmptyAux1 : VerbPath"""
        # TODO
        raise NotImplementedError

    def p_production_172(self, p):
        """PropertyListPathNotEmptyAux1 : VerbSimple"""
        p[0] = p[1]

    def p_production_173(self, p):
        """PropertyListPathNotEmptyAux2 : SYMB_SEMICOLON PropertyListPathNotEmptyAux3"""
        p[0] = p[2]

    def p_production_174(self, p):
        """PropertyListPathNotEmptyAux2 : empty"""
        p[0] = []

    def p_production_175(self, p):
        """PropertyListPathNotEmptyAux3 : PropertyListPathNotEmptyAux1 ObjectList"""
        subs = []
        for obj in p[2]:
            subs.append((p[1], obj))
        p[0] = subs

    def p_production_176(self, p):
        """PropertyListPathNotEmptyAux3 : empty"""
        p[0] = []

    def p_production_178(self, p):
        """VerbPath : Path"""
        # TODO
        raise NotImplementedError

    def p_production_180(self, p):
        """VerbSimple : Var"""
        p[0] = p[1].name

    def p_production_182(self, p):
        """ObjectListPath : ObjectPath ObjectListPathAux"""
        objs = [p[1]]
        if p[2] is not None:
            objs.append(p[2])

        p[0] = objs

    def p_production_183(self, p):
        """ObjectListPathAux : SYMB_COMMA ObjectPath"""
        p[0] = p[2]

    def p_production_184(self, p):
        """ObjectListPathAux : empty"""
        pass

    def p_production_186(self, p):
        """ObjectPath : GraphNodePath"""
        p[0] = p[1]

    def p_production_188(self, p):
        """Path : PathAlternative"""
        # TODO
        raise NotImplementedError

    def p_production_190(self, p):
        """PathAlternative : PathSequence PathAlternativeAux"""
        # TODO
        raise NotImplementedError

    def p_production_191(self, p):
        """PathAlternativeAux : SYMB_PIPE PathSequence PathAlternativeAux"""
        # TODO
        raise NotImplementedError

    def p_production_192(self, p):
        """PathAlternativeAux : empty"""
        # TODO
        raise NotImplementedError

    def p_production_194(self, p):
        """PathSequence : PathEltOrInverse PathSequenceAux"""
        # TODO
        raise NotImplementedError

    def p_production_195(self, p):
        """PathSequenceAux : SYMB_SLASH PathEltOrInverse PathSequenceAux"""
        # TODO
        raise NotImplementedError

    def p_production_196(self, p):
        """PathSequenceAux : empty"""
        # TODO
        raise NotImplementedError

    def p_production_198(self, p):
        """PathElt : PathPrimary PathEltAux"""
        # TODO
        raise NotImplementedError

    def p_production_199(self, p):
        """PathEltAux : PathMod"""
        # TODO
        raise NotImplementedError

    def p_production_200(self, p):
        """PathEltAux : empty"""
        # TODO
        raise NotImplementedError

    def p_production_202(self, p):
        """PathEltOrInverse : PathElt"""
        # TODO
        raise NotImplementedError

    def p_production_203(self, p):
        """PathEltOrInverse : SYMB_CIRCUMFLEX PathElt"""
        # TODO
        raise NotImplementedError

    def p_production_205(self, p):
        """PathMod : SYMB_QUESTION"""
        # TODO
        raise NotImplementedError

    def p_production_206(self, p):
        """PathMod : SYMB_ASTERISK"""
        # TODO
        raise NotImplementedError

    def p_production_207(self, p):
        """PathMod : SYMB_PLUS"""
        # TODO
        raise NotImplementedError

    def p_production_209(self, p):
        """PathPrimary : iri"""
        # TODO
        raise NotImplementedError

    def p_production_210(self, p):
        """PathPrimary : SYMB_a"""
        # TODO
        raise NotImplementedError

    def p_production_211(self, p):
        """PathPrimary : SYMB_EXCLAMATION PathNegatedPropertySet"""
        # TODO
        raise NotImplementedError

    def p_production_212(self, p):
        """PathPrimary : SYMB_LP Path SYMB_RP"""
        # TODO
        raise NotImplementedError

    def p_production_215(self, p):
        """PathNegatedPropertySet : PathOneInPropertySet"""
        # TODO
        raise NotImplementedError

    def p_production_216(self, p):
        """PathNegatedPropertySet : SYMB_LP PathNegatedPropertySetAux1 SYMB_RP"""
        # TODO
        raise NotImplementedError

    def p_production_217(self, p):
        """PathNegatedPropertySetAux1 : PathOneInPropertySet PathNegatedPropertySetAux2"""
        # TODO
        raise NotImplementedError

    def p_production_218(self, p):
        """PathNegatedPropertySetAux1 : empty"""
        # TODO
        raise NotImplementedError

    def p_production_219(self, p):
        """PathNegatedPropertySetAux2 : SYMB_PIPE PathOneInPropertySet PathNegatedPropertySetAux2"""
        # TODO
        raise NotImplementedError

    def p_production_220(self, p):
        """PathNegatedPropertySetAux2 : empty"""
        # TODO
        raise NotImplementedError

    def p_production_222(self, p):
        """PathOneInPropertySet : iri"""
        # TODO
        raise NotImplementedError

    def p_production_223(self, p):
        """PathOneInPropertySet : SYMB_a"""
        # TODO
        raise NotImplementedError

    def p_production_224(self, p):
        """PathOneInPropertySet : SYMB_CIRCUMFLEX PathOneInPropertySetAux"""
        # TODO
        raise NotImplementedError

    def p_production_225(self, p):
        """PathOneInPropertySetAux : iri"""
        # TODO
        raise NotImplementedError

    def p_production_226(self, p):
        """PathOneInPropertySetAux : SYMB_a"""
        # TODO
        raise NotImplementedError

    def p_production_228(self, p):
        """TriplesNode : Collection"""
        # TODO
        raise NotImplementedError

    def p_production_229(self, p):
        """TriplesNode : BlankNodePropertyList"""
        # TODO
        raise NotImplementedError

    def p_production_231(self, p):
        """BlankNodePropertyList : SYMB_LSB PropertyListNotEmpty SYMB_RSB"""
        # TODO
        raise NotImplementedError

    def p_production_233(self, p):
        """TriplesNodePath : CollectionPath"""
        # TODO
        raise NotImplementedError

    def p_production_234(self, p):
        """TriplesNodePath : BlankNodePropertyListPath"""
        # TODO
        raise NotImplementedError

    def p_production_236(self, p):
        """BlankNodePropertyListPath : SYMB_LSB PropertyListPathNotEmpty SYMB_RSB"""
        # TODO
        raise NotImplementedError

    def p_production_238(self, p):
        """Collection : SYMB_LP GraphNode CollectionAux SYMB_RP"""
        # TODO
        raise NotImplementedError

    def p_production_239(self, p):
        """CollectionAux : GraphNode CollectionAux"""
        # TODO
        raise NotImplementedError

    def p_production_240(self, p):
        """CollectionAux : empty"""
        # TODO
        raise NotImplementedError

    def p_production_242(self, p):
        """CollectionPath : SYMB_LP GraphNodePath CollectionPathAux SYMB_RP"""
        # TODO
        raise NotImplementedError

    def p_production_243(self, p):
        """CollectionPathAux : GraphNodePath CollectionPathAux"""
        # TODO
        raise NotImplementedError

    def p_production_244(self, p):
        """CollectionPathAux : empty"""
        # TODO
        raise NotImplementedError

    def p_production_246(self, p):
        """GraphNode : TriplesNode"""
        p[0] = p[1]

    def p_production_247(self, p):
        """GraphNode : VarOrTerm"""
        p[0] = p[1]

    def p_production_249(self, p):
        """GraphNodePath : VarOrTerm"""
        p[0] = p[1]

    def p_production_250(self, p):
        """GraphNodePath : TriplesNodePath"""
        p[0] = p[1]

    def p_production_252(self, p):
        """VarOrTerm : Var"""
        p[0] = p[1].name

    def p_production_253(self, p):
        """VarOrTerm : GraphTerm"""
        p[0] = p[1]

    def p_production_255(self, p):
        """VarOrIri : Var"""
        p[0] = p[1]

    def p_production_256(self, p):
        """VarOrIri : iri"""
        p[0] = p[1]

    def p_production_258(self, p):
        """Var : VAR1
               | VAR2"""
        p[0] = nodes.Var(p[1], False)
        self.query.variables.append(p[0])

    def p_production_261(self, p):
        """GraphTerm : iri"""
        p[0] = p[1]

    def p_production_262(self, p):
        """GraphTerm : RDFLiteral"""
        p[0] = p[1]

    def p_production_263(self, p):
        """GraphTerm : NumericLiteral"""
        p[0] = p[1]

    def p_production_264(self, p):
        """GraphTerm : BooleanLiteral"""
        p[0] = p[1]

    def p_production_265(self, p):
        """GraphTerm : BlankNode"""
        p[0] = None

    def p_production_266(self, p):
        """GraphTerm : NIL"""
        p[0] = None

    def p_production_268(self, p):
        """Expression : ConditionalOrExpression"""
        p[0] = nodes.ExpressionNode(p[1])

    def p_production_270(self, p):
        """ConditionalOrExpression : ConditionalAndExpression ConditionalOrExpressionAux"""
        p[0] = nodes.OrExpression(p[1], p[2])

    def p_production_271(self, p):
        """ConditionalOrExpressionAux : SYMB_OR ConditionalAndExpression ConditionalOrExpressionAux"""
        p[0] = [p[2], *p[3]]

    def p_production_272(self, p):
        """ConditionalOrExpressionAux : empty"""
        p[0] = []

    def p_production_274(self, p):
        """ConditionalAndExpression : ValueLogical ConditionalAndExpressionAux"""
        p[0] = nodes.AndExpression(p[1], p[2])

    def p_production_275(self, p):
        """ConditionalAndExpressionAux : SYMB_AND ValueLogical ConditionalAndExpressionAux"""
        p[0] = [p[2], *p[3]]

    def p_production_276(self, p):
        """ConditionalAndExpressionAux : empty"""
        p[0] = []

    def p_production_278(self, p):
        """ValueLogical : RelationalExpression"""
        p[0] = p[1]

    def p_production_280(self, p):
        """RelationalExpression : NumericExpression RelationalExpressionAux"""
        p[0] = nodes.RelationalExpression(p[1], p[2])

    def p_production_281(self, p):
        """RelationalExpressionAux : SYMB_EQ NumericExpression"""
        p[0] = (nodes.LogOperator.EQ, p[2])

    def p_production_282(self, p):
        """RelationalExpressionAux : SYMB_NEQ NumericExpression"""
        p[0] = (nodes.LogOperator.NEQ, p[2])

    def p_production_283(self, p):
        """RelationalExpressionAux : SYMB_LT NumericExpression"""
        p[0] = (nodes.LogOperator.LT, p[2])

    def p_production_284(self, p):
        """RelationalExpressionAux : SYMB_GT NumericExpression"""
        p[0] = (nodes.LogOperator.GT, p[2])

    def p_production_285(self, p):
        """RelationalExpressionAux : SYMB_LTE NumericExpression"""
        p[0] = (nodes.LogOperator.LTE, p[2])

    def p_production_286(self, p):
        """RelationalExpressionAux : SYMB_GTE NumericExpression"""
        p[0] = (nodes.LogOperator.GTE, p[2])

    def p_production_287(self, p):
        """RelationalExpressionAux : KW_IN ExpressionList"""
        p[0] = (nodes.LogOperator.IN, p[2])

    def p_production_288(self, p):
        """RelationalExpressionAux : KW_NOT KW_IN ExpressionList"""
        p[0] = (nodes.LogOperator.NOT_IN, p[2])

    def p_production_289(self, p):
        """RelationalExpressionAux : empty"""
        p[0] = None

    def p_production_291(self, p):
        """NumericExpression : AdditiveExpression"""
        p[0] = p[1]

    def p_production_292(self, p):
        """AdditiveExpression : MultiplicativeExpression AdditiveExpressionAux1"""
        p[0] = nodes.AdditiveExpression(p[1], *p[2])

    def p_production_293(self, p):
        """AdditiveExpressionAux1 : SYMB_PLUS MultiplicativeExpression AdditiveExpressionAux1"""
        p[0] = [(nodes.AdditiveOperator.SUB, p[2]), *p[3]]

    def p_production_294(self, p):
        """AdditiveExpressionAux1 : SYMB_MINUS MultiplicativeExpression AdditiveExpressionAux1"""
        p[0] = [(nodes.AdditiveOperator.SUB, p[2]), *p[3]]

    def p_production_295(self, p):
        """AdditiveExpressionAux1 : empty"""
        p[0] = []

    def p_production_304(self, p):
        """MultiplicativeExpression : UnaryExpression MultiplicativeExpressionAux"""
        p[0] = nodes.MultiplicativeExpression(p[1], p[2])

    def p_production_305(self, p):
        """MultiplicativeExpressionAux : SYMB_ASTERISK UnaryExpression MultiplicativeExpressionAux"""
        p[0] = [(nodes.MultiplicativeOperator.MULT, p[2]), *p[3]]

    def p_production_306(self, p):
        """MultiplicativeExpressionAux : SYMB_SLASH UnaryExpression MultiplicativeExpressionAux"""
        p[0] = [(nodes.MultiplicativeOperator.DIV, p[2]), *p[3]]

    def p_production_307(self, p):
        """MultiplicativeExpressionAux : empty"""
        p[0] = []

    def p_production_309(self, p):
        """UnaryExpression : SYMB_EXCLAMATION PrimaryExpression"""
        p[0] = nodes.UnaryExpression(nodes.UnaryOperator.NOT, p[1])

    def p_production_310(self, p):
        """UnaryExpression : SYMB_PLUS PrimaryExpression"""
        p[0] = nodes.UnaryExpression(nodes.UnaryOperator.PLUS, p[1])

    def p_production_311(self, p):
        """UnaryExpression : SYMB_MINUS PrimaryExpression"""
        p[0] = nodes.UnaryExpression(nodes.UnaryOperator.MINUS, p[1])

    def p_production_312(self, p):
        """UnaryExpression : PrimaryExpression"""
        p[0] = nodes.UnaryExpression(None, p[1])

    def p_production_314(self, p):
        """PrimaryExpression : BrackettedExpression"""
        p[0] = nodes.PrimaryExpression(nodes.PrimaryType.EXP, p[1])

    def p_production_315(self, p):
        """PrimaryExpression : BuiltInCall"""
        p[0] = p[1]

    def p_production_316(self, p):
        """PrimaryExpression : iri"""
        p[0] = nodes.PrimaryExpression(nodes.PrimaryType.IRI, p[1])

    def p_production_317(self, p):
        """PrimaryExpression : RDFLiteral"""
        p[0] = nodes.PrimaryExpression(nodes.PrimaryType.RDF_LITERAL, p[1])

    def p_production_318(self, p):
        """PrimaryExpression : NumericLiteral"""
        p[0] = nodes.PrimaryExpression(nodes.PrimaryType.NUM_LITERAL, p[1])

    def p_production_319(self, p):
        """PrimaryExpression : BooleanLiteral"""
        p[0] = nodes.PrimaryExpression(nodes.PrimaryType.BOOL_LITERAL, p[1])

    def p_production_320(self, p):
        """PrimaryExpression : Var"""
        p[0] = nodes.PrimaryExpression(nodes.PrimaryType.VAR, p[1])

    def p_production_322(self, p):
        """BrackettedExpression : SYMB_LP Expression SYMB_RP"""
        p[0] = p[2]

    def p_production_324(self, p):
        """BuiltInCall : Aggregate"""
        p[0] = p[1]

    def p_production_325(self, p):
        """BuiltInCall : FUNC_RAND NIL"""
        p[0] = nodes.BuiltInFunction('RAND', [])

    def p_production_326(self, p):
        """BuiltInCall : FUNC_ABS SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('ABS', [p[3]])

    def p_production_327(self, p):
        """BuiltInCall : FUNC_CEIL SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('CEIL', [p[3]])

    def p_production_328(self, p):
        """BuiltInCall : FUNC_FLOOR SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('FLOOR', [p[3]])

    def p_production_329(self, p):
        """BuiltInCall : FUNC_ROUND SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('ROUND', [p[3]])

    def p_production_330(self, p):
        """BuiltInCall : FUNC_CONCAT ExpressionList"""
        p[0] = nodes.BuiltInFunction('CONCAT', p[2])

    def p_production_331(self, p):
        """BuiltInCall : SubstringExpression"""
        p[0] = p[1]

    def p_production_332(self, p):
        """BuiltInCall : FUNC_STRLEN SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('STRLEN', [p[3]])

    def p_production_333(self, p):
        """BuiltInCall : StrReplaceExpression"""
        p[0] = p[1]

    def p_production_334(self, p):
        """BuiltInCall : FUNC_UCASE SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('UCASE', [p[3]])

    def p_production_335(self, p):
        """BuiltInCall : FUNC_LCASE SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('LCASE', [p[3]])

    def p_production_336(self, p):
        """BuiltInCall : FUNC_CONTAINS SYMB_LP Expression SYMB_COMMA Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('CONTAINS', [p[3], p[5]])

    def p_production_337(self, p):
        """BuiltInCall : FUNC_STRSTARTS SYMB_LP Expression SYMB_COMMA Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('STRSTARTS', [p[3], p[5]])

    def p_production_338(self, p):
        """BuiltInCall : FUNC_STRENDS SYMB_LP Expression SYMB_COMMA Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('STRENDS', [p[3], p[5]])

    def p_production_339(self, p):
        """BuiltInCall : FUNC_YEAR SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('YEAR', [p[3]])

    def p_production_340(self, p):
        """BuiltInCall : FUNC_MONTH SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('MONTH', [p[3]])

    def p_production_341(self, p):
        """BuiltInCall : FUNC_DAY SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('DAY', [p[3]])

    def p_production_342(self, p):
        """BuiltInCall : FUNC_HOURS SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('HOURS', [p[3]])

    def p_production_343(self, p):
        """BuiltInCall : FUNC_MINUTES SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('MINUTES', [p[3]])

    def p_production_344(self, p):
        """BuiltInCall : FUNC_SECONDS SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('SECONDS', [p[3]])

    def p_production_345(self, p):
        """BuiltInCall : FUNC_TIMEZONE SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('TIMEZONE', [p[3]])

    def p_production_346(self, p):
        """BuiltInCall : FUNC_TZ SYMB_LP Expression SYMB_RP"""
        p[0] = nodes.BuiltInFunction('TIMEZONE', [p[3]])

    def p_production_347(self, p):
        """BuiltInCall : FUNC_NOW NIL"""
        p[0] = nodes.BuiltInFunction('NOW', [])

    def p_production_348(self, p):
        """BuiltInCall : FUNC_COALESCE ExpressionList"""
        p[0] = nodes.BuiltInFunction('COALESCE', p[2])

    def p_production_349(self, p):
        """BuiltInCall : RegexExpression"""
        p[0] = p[1]

    def p_production_351(self, p):
        """RegexExpression : FUNC_REGEX SYMB_LP Expression SYMB_COMMA Expression RegexExpressionAux SYMB_RP"""
        params = [p[4], p[5]]
        params.extend(p[6])
        p[0] = nodes.BuiltInFunction('REGEX', p)

    def p_production_352(self, p):
        """RegexExpressionAux : SYMB_COMMA Expression"""
        p[0] = p[2]

    def p_production_353(self, p):
        """RegexExpressionAux : empty"""
        p[0] = []

    def p_production_355(self, p):
        """SubstringExpression : FUNC_SUBSTR SYMB_LP Expression SYMB_COMMA Expression SubstringExpressionAux SYMB_RP"""
        params = [p[4], p[5]]
        params.extend(p[6])
        p[0] = nodes.BuiltInFunction('SUBSTR', params)

    def p_production_356(self, p):
        """SubstringExpressionAux : SYMB_COMMA Expression"""
        p[0] = p[2]

    def p_production_357(self, p):
        """SubstringExpressionAux : empty"""
        p[0] = []

    def p_production_359(self, p):
        """StrReplaceExpression : FUNC_REPLACE SYMB_LP Expression SYMB_COMMA Expression SYMB_COMMA Expression StrReplaceExpressionAux SYMB_RP"""
        params = [p[4], p[5], p[7]]
        params.extend(p[8])
        p[0] = nodes.BuiltInFunction('REPLACE', params)

    def p_production_360(self, p):
        """StrReplaceExpressionAux : SYMB_COMMA Expression"""
        p[0] = p[1]

    def p_production_361(self, p):
        """StrReplaceExpressionAux : empty"""
        p[0] = []

    def p_production_363(self, p):
        """Aggregate : FUNC_COUNT SYMB_LP AggregateAux1 AggregateAux2 SYMB_RP"""
        p[0] = structures.BuiltInFunction('COUNT', [p[4]], p[3])

    def p_production_364(self, p):
        """Aggregate : FUNC_SUM SYMB_LP AggregateAux1 Expression SYMB_RP"""
        p[0] = structures.BuiltInFunction('SUM', [p[4]], p[3])

    def p_production_365(self, p):
        """Aggregate : FUNC_MIN SYMB_LP AggregateAux1 Expression SYMB_RP"""
        p[0] = structures.BuiltInFunction('MIN', [p[4]], p[3])

    def p_production_366(self, p):
        """Aggregate : FUNC_MAX SYMB_LP AggregateAux1 Expression SYMB_RP"""
        p[0] = structures.BuiltInFunction('MAX', [p[4]], p[3])

    def p_production_367(self, p):
        """Aggregate : FUNC_AVG SYMB_LP AggregateAux1 Expression SYMB_RP"""
        p[0] = structures.BuiltInFunction('AVG', [p[4]], p[3])

    def p_production_368(self, p):
        """AggregateAux1 : KW_DISTINCT"""
        p[0] = [p[1]]

    def p_production_369(self, p):
        """AggregateAux1 : empty"""
        p[0] = None

    def p_production_370(self, p):
        """AggregateAux2 : SYMB_ASTERISK"""
        p[0] = p[1]

    def p_production_371(self, p):
        """AggregateAux2 : Expression"""
        p[0] = p[1]

    def p_production_373(self, p):
        """RDFLiteral : String RDFLiteralAux1"""
        p[0] = p[1] + p[2]

    def p_production_374(self, p):
        """RDFLiteralAux1 : LANGTAG"""
        p[0] = '@' + p[1]

    def p_production_375(self, p):
        """RDFLiteralAux1 : SYMB_C2 iri"""
        p[0] = p[1] + p[2]

    def p_production_376(self, p):
        """RDFLiteralAux1 : empty"""
        p[0] = ''

    def p_production_378(self, p):
        """NumericLiteral : NumericLiteralUnsigned"""
        p[0] = p[1]

    def p_production_379(self, p):
        """NumericLiteral : NumericLiteralPositive"""
        p[0] = p[1]

    def p_production_380(self, p):
        """NumericLiteral : NumericLiteralNegative"""
        p[0] = p[1]

    def p_production_382(self, p):
        """NumericLiteralUnsigned : INTEGER"""
        p[0] = int(p[1])

    def p_production_383(self, p):
        """NumericLiteralUnsigned : DECIMAL"""
        p[0] = float(p[1])

    def p_production_384(self, p):
        """NumericLiteralUnsigned : DOUBLE"""
        p[0] = float(p[1])

    def p_production_386(self, p):
        """NumericLiteralPositive : INTEGER_POSITIVE"""
        p[0] = int(p[1])

    def p_production_387(self, p):
        """NumericLiteralPositive : DECIMAL_POSITIVE"""
        p[0] = float(p[1])

    def p_production_388(self, p):
        """NumericLiteralPositive : DOUBLE_POSITIVE"""
        p[0] = float(p[1])

    def p_production_390(self, p):
        """NumericLiteralNegative : INTEGER_NEGATIVE"""
        p[0] = int(p[1])

    def p_production_391(self, p):
        """NumericLiteralNegative : DECIMAL_NEGATIVE"""
        p[0] = float(p[1])

    def p_production_392(self, p):
        """NumericLiteralNegative : DOUBLE_NEGATIVE"""
        p[0] = float(p[1])

    def p_production_394(self, p):
        """BooleanLiteral : SYMB_TRUE"""
        p[0] = True

    def p_production_395(self, p):
        """BooleanLiteral : SYMB_FALSE"""
        p[0] = False

    def p_production_397(self, p):
        """String : STRING_LITERAL1"""
        p[0] = p[1]

    def p_production_398(self, p):
        """String : STRING_LITERAL2"""
        p[0] = p[1]

    def p_production_399(self, p):
        """String : STRING_LITERAL_LONG1"""
        p[0] = p[1]

    def p_production_400(self, p):
        """String : STRING_LITERAL_LONG2"""
        p[0] = p[1]

    def p_production_402(self, p):
        """iri : IRIREF"""
        p[0] = structures.PrimaryExpression(structures.PrimaryType.IRI, p[1])

    def p_production_403(self, p):
        """iri : PrefixedName"""
        p[0] = structures.PrimaryExpression(structures.PrimaryType.IRI, p[1])

    def p_production_405(self, p):
        """PrefixedName : PNAME_LN"""
        p[0] = p[1]

    def p_production_406(self, p):
        """PrefixedName : PNAME_NS"""
        p[0] = p[1]

    def p_production_408(self, p):
        """BlankNode : BLANK_NODE_LABEL"""
        p[0] = ""

    def p_production_409(self, p):
        """BlankNode : ANON"""
        p[0] = ""

    def p_empty(self, p):
        """empty :"""
        pass

    def p_error(self, p):
        print('ERROR!')
        print(p)
