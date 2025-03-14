import unittest
from Client_Helper import exponent_mod
from Client_Helper import aes_ctr_prg
from Client_Helper import maskModel, aes_ctr_prg, exponent_mod
# filepath: /c:/Users/nguye/OneDrive/Desktop/New folder/Module_DATN/Modules/test_Client_Helper.py

class TestClientHelper(unittest.TestCase):
  
  def test_exponent_mod_basic(self):
    self.assertEqual(exponent_mod(2, 3, 5), 3)
    self.assertEqual(exponent_mod(3, 3, 7), 6)
    self.assertEqual(exponent_mod(10, 2, 6), 4)
  
  def test_exponent_mod_large_exponent(self):
    self.assertEqual(exponent_mod(2, 1000, 13), 3)
    self.assertEqual(exponent_mod(5, 200, 23), 2)
  
  def test_exponent_mod_large_base(self):
    self.assertEqual(exponent_mod(123456789, 2, 1000000007), 643499475)
  
  def test_exponent_mod_edge_cases(self):
    self.assertEqual(exponent_mod(0, 0, 1), 0)
    self.assertEqual(exponent_mod(1, 0, 1), 0)
    # self.assertEqual(exponent_mod(0, 1, 1), 0)
    # self.assertEqual(exponent_mod(1, 1, 1), 0)
    # self.assertEqual(exponent_mod(1, 1, 2), 1)


class TestAesCtrPrg(unittest.TestCase):
  def test_aes_ctr_prg(self):
      # Test case 1: Check if the function returns an integer
      result = aes_ctr_prg(12345)
      self.assertIsInstance(result, int)

      # Test case 2: Check if the function returns the correct number of bytes
      num_bytes = 8
      result = aes_ctr_prg(12345, num_bytes)
      self.assertEqual(result.bit_length() // 8 + 1, num_bytes)

      # Test case 3: Check if the function returns consistent results for the same seed
      seed = 12345
      result1 = aes_ctr_prg(seed)
      result2 = aes_ctr_prg(seed)
      self.assertEqual(result1, result2)

      # Test case 4: Check if the function returns different results for different seeds
      seed1 = 12345
      seed2 = 54321
      result1 = aes_ctr_prg(seed1)
      result2 = aes_ctr_prg(seed2)
      self.assertNotEqual(result1, result2)


class TestMaskModel(unittest.TestCase):
  # def test_mask_model(self):
  #     # Test case 1: Basic functionality
  #     wlm = 100
  #     neighbors = [(1, 3), (2, 5)]
  #     ps = 2
  #     ss = 10
  #     self_id = 1
  #     q = 7
  #     expected_result = wlm + aes_ctr_prg(ss)
  #     for neighbor_id, neighbor_public in neighbors:
  #         sign = -1 if self_id > neighbor_id else 1
  #         expected_result += sign * aes_ctr_prg(exponent_mod(neighbor_public, ps, q))
  #     self.assertEqual(maskModel(wlm, neighbors, ps, ss, self_id, q), expected_result)

  #     # Test case 2: No neighbors
  #     wlm = 50
  #     neighbors = []
  #     ps = 3
  #     ss = 5
  #     self_id = 2
  #     q = 11
  #     expected_result = wlm + aes_ctr_prg(ss)
  #     self.assertEqual(maskModel(wlm, neighbors, ps, ss, self_id, q), expected_result)

  #     # Test case 3: Single neighbor with higher ID
  #     wlm = 75
  #     neighbors = [(3, 7)]
  #     ps = 4
  #     ss = 15
  #     self_id = 2
  #     q = 13
  #     expected_result = wlm + aes_ctr_prg(ss)
  #     for neighbor_id, neighbor_public in neighbors:
  #         sign = -1 if self_id > neighbor_id else 1
  #         expected_result += sign * aes_ctr_prg(exponent_mod(neighbor_public, ps, q))
  #     self.assertEqual(maskModel(wlm, neighbors, ps, ss, self_id, q), expected_result)
  

  def test_mask_model_aggregation(self):
    # Test case: Check if masks cancel out during aggregation
    wlms = [100, 200, 300, 400]  # Local models
    client_ids = [1, 2, 3, 4]  # Client IDs
    ps_values = [3, 5, 7, 11]  # Public keys of each client
    neighbors = [[2, 3, 4], [1, 3, 4], [1, 2, 4], [1, 2, 3]]  # Each client has all others as neighbors
    ss_values = [10, 20, 30, 40]  # Self secrets for each client
    q = 19472468722417397862558857150087778833563567447828596137285949137713554888004771279233477394582204013249209520541369050915998789018565616266327796914086325427778753887468211249285574734294151829310027214581775193890142939838132633371974477813502883331360744022497806724741968550141407644231522327645042702362263231672364430967906551566700028939158562682842922050404300793021053108400897416440694342611660893657584496011521574815551724188606262074259571796638737602576098759418276877681850654914056243425729800720713560064186603082272673535566186497264161034856105408817239711481740341605347326896143605436974992107063  # Prime number for modulo operations

    # Generate correct neighbors dictionary based on provided `neighbors` list
    neighbors_dict = {
        client_id: [(neighbor_id, exponent_mod(2,ps_values[client_ids.index(neighbor_id)],q)) for neighbor_id in neighbor_list]
        for client_id, neighbor_list in zip(client_ids, neighbors)
    }
    # Compute masked models for each client using the correct neighbors
    masked_models = [
        maskModel(self_wlm, neighbors_dict[self_id], self_ps, self_ss, self_id, q)
        for self_wlm, self_ps, self_ss, self_id in zip(wlms, ps_values, ss_values, client_ids)
    ]
    # Compute unmasked models (just wlm + ss)
    unmasked_models = [wlm + aes_ctr_prg(ss) for wlm, ss in zip(wlms, ss_values)]

    # Aggregate masked models
    aggregated_masked_model = sum(masked_models)
  
    # Aggregate unmasked models
    aggregated_unmasked_model = sum(unmasked_models)

    # Check if masks cancel out after aggregation
    self.assertEqual(aggregated_masked_model, aggregated_unmasked_model)



if __name__ == '__main__':
  unittest.main()
  # print(pow(1,1,2))