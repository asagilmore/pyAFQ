import AFQ.api.bundle_dict as abd
from AFQ.tests.test_api import create_dummy_bids_path
from AFQ.api.group import GroupAFQ
import AFQ.data.fetch as afd
import pytest


def test_AFQ_custom_bundle_dict():
    bids_path = create_dummy_bids_path(3, 1)
    bundle_dict = abd.default18_bd()
    GroupAFQ(
        bids_path,
        preproc_pipeline="synthetic",
        bundle_info=bundle_dict)


def test_BundleDict():
    """
    Tests bundle dict
    """

    # test defaults
    afq_bundles = abd.default18_bd()

    assert len(afq_bundles) == len(abd.BUNDLES)

    # Arcuate Fasciculus
    afq_bundles = abd.default18_bd()["ARC_L", "ARC_R"]

    assert len(afq_bundles) == 2

    # Forceps Minor and Major
    afq_bundles = abd.default18_bd()["FA", "FP"]

    assert len(afq_bundles) == 2

    # Cingulum Hippocampus
    # not included but exists in templates
    # so this was a wierd test to have
    # we should find a reliable segmentation of these
    # afq_bundles = abd.BundleDict(["HCC_L", "HCC_R"])

    # assert len(afq_bundles) == 2

    # Test "custom" bundle
    afq_templates = afd.read_templates()
    afq_bundles = abd.BundleDict({
        "custom_bundle": {
            "include": [
                afq_templates["FA_L"],
                afq_templates["FP_R"]],
            "cross_midline": False}})
    afq_bundles.get("custom_bundle")

    assert len(afq_bundles) == 1

    # mispelled bundle that does not exist in afq templates
    with pytest.raises(
            ValueError,
            match=" is not in this BundleDict"):
        afq_bundles = abd.default18_bd()["VOQ_L", "VOQ_R"]

    afq_bundles = abd.reco_bd(80)["VOF_L", "VOF_R"]
    assert len(afq_bundles) == 2

    afq_bundles = abd.reco_bd(80)[["whole_brain"]]
    assert len(afq_bundles) == 1
