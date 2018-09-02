import unittest

import rastervision as rv

# class TestExperiment(unittest.TestCase):
#     def test_build_experiment(self):
#         task, backend, dataset =  (1, 2, 3)
#         e = rv.Experiment.builder() \
#                          .with_task(task) \
#                          .with_backend(backend) \
#                          .with_dataset(dataset) \
#                          .build()

#         self.assertEqual(e.task, task)
#         self.assertEqual(e.backend, backend)
#         self.assertEqual(e.dataset, dataset)

#     def test_build_experiment_from_existing(self):
#         task, backend, dataset =  (1, 2, 3)
#         e = rv.Experiment.builder() \
#                          .with_task(task) \
#                          .with_backend(backend) \
#                          .with_dataset(dataset) \
#                          .build()

#         dataset2 = 4
#         e2 = e.builder() \
#               .with_dataset(dataset2) \
#               .build()

#         self.assertEqual(e.dataset, dataset)
#         self.assertEqual(e2.dataset, dataset2)

if __name__ == "__main__":
    unittest.main()
