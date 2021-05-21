/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : huisuan

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 07/04/2020 11:25:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for main_update
-- ----------------------------
DROP TABLE IF EXISTS `main_update`;
CREATE TABLE `main_update`  (
  `Reference` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Reference_ID_S` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Evidence_level` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `level_1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Drug_ref` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Drug_temp` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Drug_en` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Drug_ch` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Drug` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `MAX phase` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Disease_Ref` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Disease_en` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `RelatedDisease` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `site_cosmic` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `DrugEfficacy` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `clinical_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Biomarker` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ApprovedSymbol` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Mutation_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Mutation_class` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Mutation_exon` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `AAMutation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `MutationEffect_rule` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Interpretation_1` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `Summary` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `Germline_somatic` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pro_DrugEfficacy` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `update` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `simple_explain` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `update_columns` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  UNIQUE INDEX `clinical_type`(`clinical_type`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of main_update
-- ----------------------------
INSERT INTO `main_update` VALUES ('NCCN Guideline: Soft Tissue Sarcoma <4.2019>', '.', 'guideline:NCCN', '1', 'imatinib', 'imatinib', 'imatinib', '伊马替尼', 'imatinib|伊马替尼', '4', 'Gastrointestinal Stromal Tumors', 'gastrointestinal stromal tumor', '胃肠间质瘤-to-胃肠间质瘤_test', 'na', 'sensitivity', 'EVI_000041', 'KIT:nonsynonymous SNV:exon9:.:exon9act', 'KIT', 'nonsynonymous SNV', 'None_pos', 'exon9', '.', 'exon9act', 'In patients with advanced GISTs, approximately 90% of patients benefit from imatinib when their  tumors have a KIT exon 11 mutation; approximately 50% of patients benefit from imatinib when  their tumors harbor a KIT exon 9 mutation, and the likelihood of response improves with the use of  800 mg imatinib rather than the standard 400 mg dose. Most mutations in the PDGFRA gene are  associated with a response to imatinib, with the notable exception of D842V. In the absence of KIT  and PDGFRA mutations, only a subset of patients with advanced GISTs benefit from imatinib.  Metastatic disease with acquired drug resistance is usually the result of secondary, imatinib  resistant mutations in KIT or PDGFRA.', '在GIST患者中，90%携带KIT基因11号外显子突变的患者可以从伊马替尼治疗中获益；50%携带KIT基因9号外显子突变的患者可以从伊马替尼治疗中获益，并且需要使用高剂量伊马替尼（800 mg）。除了PDGFRA D842V突变外，大部分PDGFRA基因突变都对伊马替尼敏感。在没有KIT或PDGFRA基因突变时，只有少部分患者可以从伊马替尼治疗中获益。其它发生在KIT基因上的激活突变也可能提示患者对伊马替尼敏感。', 'S', '敏感', 'o', '', '');
INSERT INTO `main_update` VALUES ('Druglabel:imatinib_Revised:01/2015', '.', 'guideline:FDA', '1', 'imatinib', 'imatinib', 'imatinib', '伊马替尼', 'imatinib|伊马替尼', '4', 'Dermatofibrosarcoma Protuberans', 'dermatofibrosarcoma protuberans', '皮肤纤维肉瘤-to-皮肤纤维肉瘤_test', 'na', 'sensitivity', 'EVI_000048', 'PDGFB:FUS:.:COL1A1-PDGFB:.', 'PDGFB', 'FUS', 'FUS', '.', 'COL1A1-PDGFB', '.', 'translocation of collagen type I alpha 1 (COL1A1; on 17q22) with platelet-derived growth factor Beta (PDGFB; on 22q13) to form the oncogenic chimeric fusion gene t(17;22)(q22;q13).', '携带COL1A1与PDGFB形成融合基因肿瘤的患者对伊马替尼治疗敏感。隆突性皮肤纤维肉瘤(DFSP)是一种皮肤性软组织肉瘤，其特点是携带17号染色体和22号染色体易位引起的COL1A1-PDGFB基因融合。在一项开放性、多中心、Ⅱ期临床试验中探究了伊马替尼对Abl, Kit或PDGFR蛋白激酶相关的生命威胁性疾病的作用。在这项研究中有12名DFSP患者，接受每日剂量800 mg伊马替尼。这些患者在参组治疗时患有初始手术切除后转移性、局部复发的DFSP，且不适宜进一步手术治疗。另有5篇文献中报道的6名DFSP患者也接受了伊马替尼治疗。因此，总共有18名DFSP患者，其中8名患者患有转移性疾病，文献中报道的成人患者为每日剂量400 mg或800 mg。一位儿童患者每日剂量为400 mg/m2，随后增加至520 mg/m2。18名患者中有10名患者携带PDGFB基因重排，5名患者没有有效细胞遗传学信息，3名患者携带有复杂的细胞遗传学异常。在18名患者中，有12名患者获得完全缓解（N=7）或部分缓解后通过手术使疾病消除（N=5，包括一名儿童），总的完全缓解率67%。另有3名患者获得了部分缓解，因此总缓解为83%。在8名转移性疾病患者中，5位获得部分缓解，3为获得完全缓解。在10名携带PDGFB基因重排的患者中，4名获得完全缓解，6名获得部分缓解。在临床试验中患者的中位持续缓解时间为6.2个月，最长持续时间为24.3个月，而文献中报道的中位持续缓解时间为4周~20+个月。', 'F', '敏感', 'o', '', '');

SET FOREIGN_KEY_CHECKS = 1;
