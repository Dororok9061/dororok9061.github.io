window.PORTAL_DATA = {
  "paper_title": "Research Publication Workbench",
  "subtitle": "A reusable GitHub Pages and Notion publishing portal for papers, projects, blogs, assignments, and study notes.",
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
    "Template structure adapted from the iNdra YAML-driven research page layout.",
    "PCB Visual Inspection Studio is included as the first evidence-gated case study."
  ],
  "header_note": "The visual language uses Material Symbols, strict square figures, and source-checked figure planning.",
  "buttons": [
    {
      "label": "Paper",
      "icon": "article",
      "url": "../../paper/PCB_VISUAL_INSPECTION_STUDIO_PAPER_EN.md"
    },
    {
      "label": "PDF",
      "icon": "picture_as_pdf",
      "url": "../../paper/PCB_VISUAL_INSPECTION_STUDIO_FULL_EN_WITH_PAPER_STYLE_ATLAS.pdf"
    },
    {
      "label": "Atlas",
      "icon": "view_carousel",
      "url": "../paper_style_atlas/README.md"
    },
    {
      "label": "Public Hub",
      "icon": "hub",
      "url": "https://dororok9061.github.io/"
    },
    {
      "label": "GitHub Repo",
      "icon": "code",
      "url": "https://github.com/Dororok9061/PCB-Visual-Inspection-Studio"
    },
    {
      "label": "Figures",
      "icon": "image",
      "url": "../../figure_index.md"
    },
    {
      "label": "Notion Hub",
      "icon": "dashboard",
      "url": "https://fierce-rodent-308.notion.site/Engineering-Portfolio-FPGA-Radar-Embedded-Systems-Biomedical-AI-3ab518ac7a598121b666e4c7cce8324c"
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
      "label": "Paper-style figures",
      "value": "62",
      "note": "individual PCB figures, no bundled board"
    },
    {
      "label": "Tables",
      "value": "30",
      "note": "registry-backed"
    },
    {
      "label": "PDF pages",
      "value": "112/115",
      "note": "KO/EN papers with 62-page atlas"
    },
    {
      "label": "Portal modes",
      "value": "5",
      "note": "paper, project, blog, assignment, study"
    }
  ],
  "sections": [
    {
      "id": "abstract",
      "title": "Abstract",
      "nav_label": "Abstract",
      "icon": "summarize",
      "content": "This portal turns the PCB Visual Inspection Studio publication package into a reusable research-page system. The structure follows the iNdra-style YAML editing model while widening the scope beyond one PCB paper: papers, software projects, blog posts, assignments, and study notes share the same navigation, button, gallery, evidence, and citation components.",
      "components": [
        {
          "type": "image_gallery",
          "title": "Portal Overview",
          "images": [
            "AssetsWeb/research_portal_matrix.webp",
            "AssetsWeb/pcb_overview.webp",
            "AssetsWeb/github_notion_loop.webp"
          ]
        }
      ]
    },
    {
      "id": "methodology",
      "title": "Methodology",
      "nav_label": "Methodology",
      "icon": "account_tree",
      "content": "The page is controlled by data.yaml, rendered by script.js, styled by style.css, and decorated with Material Symbols. Missing or rebuilt visual material is planned from source evidence and reviewed before publication, while each final PCB figure is published as its own strict-square image card with click-to-enlarge viewing.",
      "components": [
        {
          "type": "image_gallery",
          "title": "Separate PCB Methodology Figure Cards",
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
          "title": "1. Reusable Content Model",
          "content": "Each item is represented as a card with a type, status, figure, source link, and next action.",
          "list_type": "check",
          "list": [
            "Research papers keep abstract/method/results/citation sections.",
            "Projects keep code, docs, releases, and reproducibility links.",
            "Blog, assignment, and study entries keep short summaries and learning evidence."
          ]
        },
        {
          "title": "2. Split-Figure Publication Rule",
          "content": "Reference bundles are used only as layout grammar. The homepage, GitHub README, Notion package, and paper atlas link the rebuilt PCB figures one by one instead of publishing a combined contact sheet."
        }
      ]
    },
    {
      "id": "paper-style-atlas",
      "title": "Paper-Style Figure Atlas",
      "nav_label": "Atlas",
      "icon": "view_carousel",
      "content": "The atlas redraws the visual structures shown in the provided DINOv3, ViT, FR-PatchCore, U-ViT, TTM, TimeXer, and iTransformer examples, then inserts PCB inspection patches, heat maps, defect scores, attention maps, and evidence-scoped tables. The reference papers are used as layout grammar only; the content is regenerated for this PCB project.",
      "components": [
        {
          "type": "image_gallery",
          "title": "Copied-Structure PCB Figures",
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
      "content": "The current PCB work remains the first concrete case study. It includes strict-square figures, source-domain PatchCore/DINO pilot evidence, CUDA-oriented training records, camera-probe evidence, and explicit production gates.",
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
      "title": "Reusable Portfolio Tracks",
      "nav_label": "Tracks",
      "icon": "view_kanban",
      "content": "The same page can be reused for a publication website, GitHub project homepage, Notion portfolio summary, technical blog series, assignment archive, or study notebook index.",
      "cards": [
        {
          "type": "Paper",
          "icon": "article",
          "title": "Research Paper",
          "text": "Use Abstract, Methodology, Results, Figures, BibTeX, and PDF buttons."
        },
        {
          "type": "Project",
          "icon": "terminal",
          "title": "Software Project",
          "text": "Use setup, architecture, release, issue, and reproducibility sections."
        },
        {
          "type": "Blog",
          "icon": "edit_note",
          "title": "Blog Series",
          "text": "Use short cards, figure galleries, and incremental changelog notes."
        },
        {
          "type": "Assignment",
          "icon": "task_alt",
          "title": "Course Work",
          "text": "Use problem, method, result, artifact, and reflection fields."
        },
        {
          "type": "Study",
          "icon": "school",
          "title": "Study Notes",
          "text": "Use reading logs, concepts, diagrams, and future-question lists."
        }
      ]
    },
    {
      "id": "results",
      "title": "Results and Deliverables",
      "nav_label": "Results",
      "icon": "analytics",
      "content": "The current deliverable set contains bilingual papers, PDFs, figures, tables, equations, GitHub copy, Notion copy, blog entries, and this homepage scaffold. Claims remain evidence-gated rather than overstated.",
      "table": [
        {
          "Artifact": "Korean paper",
          "Status": "generated",
          "Path": "docs/paper/PCB_VISUAL_INSPECTION_STUDIO_PAPER_KO.md"
        },
        {
          "Artifact": "English paper",
          "Status": "generated",
          "Path": "docs/paper/PCB_VISUAL_INSPECTION_STUDIO_PAPER_EN.md"
        },
        {
          "Artifact": "Figure pack",
          "Status": "QA pass",
          "Path": "docs/AssetsWeb/figures"
        },
        {
          "Artifact": "Notion portfolio",
          "Status": "markdown ready",
          "Path": "docs/publishing/notion"
        },
        {
          "Artifact": "GitHub Pages portal",
          "Status": "template rebuild",
          "Path": "docs/publishing/homepage"
        }
      ]
    },
    {
      "id": "citation",
      "title": "Citation",
      "nav_label": "Citation",
      "icon": "format_quote",
      "content": "Use the citation block for the PCB case study or replace it in data.yaml for another paper.",
      "bibtex": "@misc{rok2026pcbworkbench,\\n  title={PCB Visual Inspection Studio and Reusable Research Publication Workbench},\\n  author={ROK Research Workspace},\\n  year={2026},\\n  note={Evidence-gated local publication package}\\n}"
    }
  ]
};
