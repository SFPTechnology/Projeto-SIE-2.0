import unittest
from datetime import date
from src.sie_normas.governance import Context, Rule, evaluate, snapshot

class GateTests(unittest.TestCase):
    def setUp(self):
        self.ctx=Context("residencial",220,"SP","EDP",date(2026,10,15),material="cobre")
        self.rule=Rule("NOR-001",1,"EDP-PENDENTE","V9","entrada",verified=True,approved=True,
            approver="revisor",effective_from=date(2024,1,1),typologies=("residencial",),
            states=("SP",),distributors=("EDP",),material="cobre",max_voltage=380)
    def test_source_unverified_blocks(self):
        self.assertEqual(evaluate(self.rule,self.ctx).status,"BLOQUEADO")
    def test_unapproved_blocks(self):
        rule=Rule(**{**self.rule.__dict__,"approved":False})
        self.assertEqual(evaluate(rule,self.ctx,source_verified=True).status,"BLOQUEADO")
    def test_wrong_distributor(self):
        ctx=Context(**{**self.ctx.__dict__,"distributor":"OUTRA"})
        self.assertEqual(evaluate(self.rule,ctx,source_verified=True).status,"NAO_APLICAVEL")
    def test_wrong_typology(self):
        ctx=Context(**{**self.ctx.__dict__,"typology":"industrial"})
        self.assertEqual(evaluate(self.rule,ctx,source_verified=True).status,"NAO_APLICAVEL")
    def test_wrong_voltage(self):
        ctx=Context(**{**self.ctx.__dict__,"voltage_v":440})
        self.assertEqual(evaluate(self.rule,ctx,source_verified=True).status,"NAO_APLICAVEL")
    def test_conflict_blocks(self):
        self.assertEqual(evaluate(self.rule,self.ctx,source_verified=True,conflict=True).status,"BLOQUEADO")
    def test_verified_record_only_eligible(self):
        self.assertEqual(evaluate(self.rule,self.ctx,source_verified=True).status,"ELEGIVEL_PARA_CALCULO")
    def test_no_effective_from_blocks(self):
        rule=Rule(**{**self.rule.__dict__,"effective_from":None})
        self.assertEqual(evaluate(rule,self.ctx,source_verified=True).status,"NAO_APLICAVEL")
    def test_revision_snapshot(self):
        self.assertEqual(snapshot(self.rule,"a"*64)["revision"],1)
        self.assertRaises(ValueError,snapshot,self.rule,"invalid")
    def test_missing_approver_blocks(self):
        rule=Rule(**{**self.rule.__dict__,"approver":None})
        self.assertEqual(evaluate(rule,self.ctx,source_verified=True).status,"BLOQUEADO")
if __name__ == "__main__": unittest.main()
