window.PORTAL_DATA = {
  "paper_title": "PCB Visual Inspection Studio",
  "subtitle": "Image quality checks, ROI registration, and anomaly detection for F411 PCB video. Explore PatchCore, FR-PatchCore, and DINOv3 feature studies through design figures and analysis records.",
  "authors": [
    {
      "name": "ROK Research Workspace",
      "superscript": "1",
      "url": "#"
    }
  ],
  "affiliations": [
    {
      "index": "1",
      "name": "Local CUDA and documentation workspace"
    }
  ],
  "conference_badges": [
    "F411 PCB inspection",
    "PatchCore · FR-PatchCore · DINOv3",
    "Design figures and local experiment records"
  ],
  "header_note": "Camera or file input → quality checks → ROI registration → feature extraction → anomaly score, heatmap, and mask.",
  "buttons": [
    {
      "label": "Project overview",
      "url": "/projects/pcb-visual-inspection/"
    },
    {
      "label": "Method figures",
      "url": "#methodology"
    },
    {
      "label": "Figure atlas",
      "url": "#paper-style-atlas"
    },
    {
      "label": "Case study",
      "url": "#case-study"
    },
    {
      "label": "All projects",
      "url": "/projects/"
    }
  ],
  "settings": {
    "max_width": "1180px",
    "nav_shadow": true,
    "nav_scroll_highlight": true,
    "nav_highlight_color": "#2454A6",
    "show_bibtex_button": true,
    "theme_toggle_text": "Theme",
    "copy_bibtex_text": "Copy BibTeX"
  },
  "metrics": [
    {
      "label": "Method figures",
      "value": "10",
      "note": "capture, ROI, features, and anomaly maps"
    },
    {
      "label": "Atlas images",
      "value": "62",
      "note": "architecture and analysis illustrations"
    },
    {
      "label": "Case-study views",
      "value": "4",
      "note": "PCB workflow and review records"
    }
  ],
  "sections": [
    {
      "id": "abstract",
      "title": "Overview",
      "nav_label": "Overview",
      "icon": "summarize",
      "content": "The inspection pipeline connects camera or file input, frame quality checks, ROI registration, feature extraction, and anomaly scores, heatmaps, and masks. This page brings together the PCB workflow, model diagrams, and analysis figures.",
      "components": [
        {
          "type": "image_gallery",
          "title": "PCB inspection overview",
          "images": [
            "AssetsWeb/pcb_overview.webp",
            "AssetsWeb/pcb_patchcore.webp",
            "AssetsWeb/pcb_detection_gate.webp"
          ]
        }
      ]
    },
    {
      "id": "methodology",
      "title": "Methods",
      "nav_label": "Methods",
      "icon": "account_tree",
      "content": "Camera and video frames pass through quality checks and ROI registration before ViT, DINO, or PatchCore-style feature extraction. Anomaly scores, heatmaps, and masks support visual review. The figures below show each stage separately.",
      "components": [
        {
          "type": "image_gallery",
          "title": "PCB method figures",
          "images": [
            "AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp",
            "AssetsWeb/paper_style/pcb_style_fig31b_vit_dino_patch_path.webp",
            "AssetsWeb/paper_style/pcb_style_fig31c_registration_memory_bank.webp",
            "AssetsWeb/paper_style/pcb_style_fig31d_heatmap_mask_fusion.webp",
            "AssetsWeb/paper_style/pcb_style_fig31e_domain_boundary.webp",
            "AssetsWeb/paper_style/pcb_style_fig31f_publication_hub_loop.webp",
            "AssetsWeb/paper_style/pcb_style_fig31g_score_distribution.webp",
            "AssetsWeb/paper_style/pcb_style_fig31h_embedding_clusters.webp",
            "AssetsWeb/paper_style/pcb_style_fig31i_loss_convergence.webp",
            "AssetsWeb/paper_style/pcb_style_fig31j_dataset_balance.webp"
          ]
        }
      ],
      "subsections": [
        {
          "title": "Image input and registration",
          "content": "The workflow separates source frames from inspection ROIs, checks capture quality, and aligns board regions before feature extraction.",
          "list": [
            "Camera and file input",
            "Capture quality checks",
            "PCB ROI alignment"
          ]
        },
        {
          "title": "Features and inspection outputs",
          "content": "PatchCore, FR-PatchCore, and DINOv3 studies connect patch features and memory-bank comparisons to anomaly maps and masks. Production evaluation criteria include gold-label comparison, defect decisions, and yield."
        }
      ]
    },
    {
      "id": "paper-style-atlas",
      "title": "PCB Figure Atlas",
      "nav_label": "Atlas",
      "icon": "view_carousel",
      "content": "PCB-focused explanatory diagrams use visual layouts from DINOv3, ViT, FR-PatchCore, U-ViT, TTM, TimeXer, and iTransformer references. The atlas covers patch features, registration, attention, memory banks, heatmaps, and analysis-table layouts. Reference architectures are listed below.",
      "components": [
        {
          "type": "image_gallery",
          "title": "Architecture and analysis illustrations",
          "images": [
            "AssetsWeb/paper_style/pcb_style_fig01_dinov3_overview.webp",
            "AssetsWeb/paper_style/pcb_style_fig02_scaling_bubbles.webp",
            "AssetsWeb/paper_style/pcb_style_fig03_dense_feature_gallery.webp",
            "AssetsWeb/paper_style/pcb_style_fig04_resolution_features.webp",
            "AssetsWeb/paper_style/pcb_style_fig05_cls_patch_similarity.webp",
            "AssetsWeb/paper_style/pcb_style_fig06_feature_evolution.webp",
            "AssetsWeb/paper_style/pcb_style_fig07_loss_curves.webp",
            "AssetsWeb/paper_style/pcb_style_fig08_benchmark_curves.webp",
            "AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp",
            "AssetsWeb/paper_style/pcb_style_fig10_registration_block.webp",
            "AssetsWeb/paper_style/pcb_style_fig11_feature_levels.webp",
            "AssetsWeb/paper_style/pcb_style_fig12_sppm_structure.webp",
            "AssetsWeb/paper_style/pcb_style_fig13_heatmap_gt_mask.webp",
            "AssetsWeb/paper_style/pcb_style_fig14_threshold_masks.webp",
            "AssetsWeb/paper_style/pcb_style_fig15_dataset_examples.webp",
            "AssetsWeb/paper_style/pcb_style_fig16_pro_line_chart.webp",
            "AssetsWeb/paper_style/pcb_style_fig17_feature_vis_compare.webp",
            "AssetsWeb/paper_style/pcb_style_fig18_loss_convergence.webp",
            "AssetsWeb/paper_style/pcb_style_fig19_qualitative_grid.webp",
            "AssetsWeb/paper_style/pcb_style_fig20_vit_model_overview.webp",
            "AssetsWeb/paper_style/pcb_style_fig21_vit_patch_sequence.webp",
            "AssetsWeb/paper_style/pcb_style_fig22_transfer_scaling_plot.webp",
            "AssetsWeb/paper_style/pcb_style_fig23_fewshot_scaling_plot.webp",
            "AssetsWeb/paper_style/pcb_style_fig24_compute_performance.webp",
            "AssetsWeb/paper_style/pcb_style_fig25_embedding_filters.webp",
            "AssetsWeb/paper_style/pcb_style_fig26_input_attention.webp",
            "AssetsWeb/paper_style/pcb_style_fig27_prediction_strip.webp",
            "AssetsWeb/paper_style/pcb_style_fig28_tsne_embeddings.webp",
            "AssetsWeb/paper_style/pcb_style_fig29_layer_attention_maps.webp",
            "AssetsWeb/paper_style/pcb_style_fig30_cross_attention_architecture.webp",
            "AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp",
            "AssetsWeb/paper_style/pcb_style_fig31b_vit_dino_patch_path.webp",
            "AssetsWeb/paper_style/pcb_style_fig31c_registration_memory_bank.webp",
            "AssetsWeb/paper_style/pcb_style_fig31d_heatmap_mask_fusion.webp",
            "AssetsWeb/paper_style/pcb_style_fig31e_domain_boundary.webp",
            "AssetsWeb/paper_style/pcb_style_fig31f_publication_hub_loop.webp",
            "AssetsWeb/paper_style/pcb_style_fig31g_score_distribution.webp",
            "AssetsWeb/paper_style/pcb_style_fig31h_embedding_clusters.webp",
            "AssetsWeb/paper_style/pcb_style_fig31i_loss_convergence.webp",
            "AssetsWeb/paper_style/pcb_style_fig31j_dataset_balance.webp",
            "AssetsWeb/paper_style/pcb_style_fig32_exogenous_attention_series.webp",
            "AssetsWeb/paper_style/pcb_style_fig33_efficiency_bubble_plot.webp",
            "AssetsWeb/paper_style/pcb_style_fig34_forecast_self_attention.webp",
            "AssetsWeb/paper_style/pcb_style_fig35_cross_attention_maps.webp",
            "AssetsWeb/paper_style/pcb_style_fig36_head_attention_maps.webp",
            "AssetsWeb/paper_style/pcb_style_fig37_prepost_layernorm.webp",
            "AssetsWeb/paper_style/pcb_style_fig38_seq2seq_transformer.webp",
            "AssetsWeb/paper_style/pcb_style_fig39_training_curves_grid.webp",
            "AssetsWeb/paper_style/pcb_style_fig40_itransformer_views.webp",
            "AssetsWeb/paper_style/pcb_style_fig41_modified_transformer_family.webp",
            "AssetsWeb/paper_style/pcb_style_fig42_timemixer_block.webp",
            "AssetsWeb/paper_style/pcb_style_fig43_mse_comparison.webp",
            "AssetsWeb/paper_style/pcb_style_fig44_cka_correlation.webp",
            "AssetsWeb/paper_style/pcb_style_table01_training_data_metrics.webp",
            "AssetsWeb/paper_style/pcb_style_table02_result_tables.webp",
            "AssetsWeb/paper_style/pcb_style_table03_module_ablation.webp",
            "AssetsWeb/paper_style/pcb_style_table04_mask_iou.webp",
            "AssetsWeb/paper_style/pcb_style_table05_pooling_comparison.webp",
            "AssetsWeb/paper_style/pcb_style_table06_train_iterations.webp",
            "AssetsWeb/paper_style/pcb_style_table07_industrial_scores.webp",
            "AssetsWeb/paper_style/pcb_style_table08_average_pro.webp",
            "AssetsWeb/paper_style/pcb_style_table09_full_result.webp"
          ]
        }
      ],
      "table": [
        {
          "Reference structure": "ViT model overview",
          "PCB atlas asset": "pcb_style_fig20_vit_model_overview.webp",
          "Inserted PCB content": "ROI patches, class token, Transformer encoder"
        },
        {
          "Reference structure": "FR-PatchCore architecture",
          "PCB atlas asset": "pcb_style_fig09_frpatchcore_pipeline.webp",
          "Inserted PCB content": "registration, memory bank, similarity loss"
        },
        {
          "Reference structure": "TimeXer attention panel",
          "PCB atlas asset": "pcb_style_fig34_forecast_self_attention.webp",
          "Inserted PCB content": "camera/recipe time series and attention maps"
        },
        {
          "Reference structure": "Industrial anomaly tables",
          "PCB atlas asset": "pcb_style_table09_full_result.webp",
          "Inserted PCB content": "PCB categories, Det./Seg. columns, F411 gate boundary"
        }
      ]
    },
    {
      "id": "case-study",
      "title": "PCB Case Study",
      "nav_label": "PCB Case",
      "icon": "memory",
      "content": "The PCB case study connects source-domain PatchCore and DINO pilot records, camera-probe examples, and the criteria for evaluating the F411 inspection workflow. The figure set follows input, feature analysis, review, and release records.",
      "components": [
        {
          "type": "image_gallery",
          "title": "PCB Evidence Gallery",
          "images": [
            "AssetsWeb/pcb_overview.webp",
            "AssetsWeb/pcb_patchcore.webp",
            "AssetsWeb/pcb_detection_gate.webp",
            "AssetsWeb/pcb_release_index.webp"
          ]
        }
      ]
    },
    {
      "id": "portfolio",
      "title": "Inspection Workflow",
      "nav_label": "Workflow",
      "icon": "view_kanban",
      "content": "Follow a board image from acquisition to its inspection outputs.",
      "cards": [
        {
          "type": "01",
          "title": "Input",
          "text": "USB or industrial-camera frames and image files."
        },
        {
          "type": "02",
          "title": "Quality and ROI",
          "text": "Capture quality checks and board-region registration."
        },
        {
          "type": "03",
          "title": "Features",
          "text": "ViT, DINO, and PatchCore-style patch representations."
        },
        {
          "type": "04",
          "title": "Anomaly maps",
          "text": "Scores, heatmaps, and masks for defect-region review."
        },
        {
          "type": "05",
          "title": "Review",
          "text": "Gold-label comparison, defect decisions, and production-evaluation criteria."
        }
      ]
    },
    {
      "id": "results",
      "title": "Figures and Records",
      "nav_label": "Records",
      "icon": "analytics",
      "content": "Available material includes PCB architecture diagrams, feature-analysis illustrations, and local experiment records. The project overview connects these materials to the inspection pipeline.",
      "table": [
        {
          "Material": "Method figures",
          "Coverage": "10 views",
          "Topics": "Capture quality, ROI, features, heatmaps, masks"
        },
        {
          "Material": "Figure atlas",
          "Coverage": "62 images",
          "Topics": "Architecture, feature analysis, and table layouts"
        },
        {
          "Material": "Case study",
          "Coverage": "4 views",
          "Topics": "PCB workflow, PatchCore, and evaluation criteria"
        }
      ]
    },
    {
      "id": "citation",
      "title": "Reference",
      "nav_label": "Reference",
      "icon": "format_quote",
      "content": "Reference for this project documentation page.",
      "bibtex": "@misc{ryu2026pcb,\n  title={PCB Visual Inspection Studio},\n  author={Hyeongrok Ryu},\n  year={2026},\n  howpublished={Project documentation},\n  url={https://dororok9061.github.io/projects/pcb-visual-inspection/}\n}"
    }
  ]
};
