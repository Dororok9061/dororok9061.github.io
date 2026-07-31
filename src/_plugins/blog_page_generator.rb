# frozen_string_literal: true

module StructuredBlog
  class GeneratedPage < Jekyll::PageWithoutAFile
    def initialize(site, dir, data)
      super(site, site.source, dir, "index.html")
      self.content = ""
      self.data = data
    end
  end

  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      generate_directories(site)
      generate_categories(site)
      generate_roadmaps(site)
      generate_english_series(site)
      generate_types(site)
    end

    private

    def add(site, dir, data)
      return if site.pages.any? { |page| page.url == "/#{dir}/" }

      site.pages << GeneratedPage.new(site, dir, data)
    end

    def generate_directories(site)
      pages = {
        "start-here" => ["처음 오셨다면", "Start Here"],
        "roadmaps" => ["분야별 학습 로드맵", "Learning Roadmaps"],
        "archive" => ["글 Archive", "Post Archive"],
        "tags" => ["표준 Tags", "Standard Tags"],
        "categories" => ["전체 카테고리", "All Categories"]
      }
      pages.each do |mode, titles|
        add(site, "blog/#{mode}", directory_data(mode, titles[0], "ko", "/en/blog/#{mode}/"))
        add(site, "en/blog/#{mode}", directory_data(mode, titles[1], "en", "/blog/#{mode}/"))
      end
    end

    def directory_data(mode, title, lang, alternate)
      {
        "layout" => "blog-directory",
        "mode" => mode,
        "title" => title,
        "description" => title,
        "lang" => lang,
        "alternate_url" => alternate,
        "alternate_lang" => lang == "en" ? "ko" : "en"
      }
    end

    def generate_categories(site)
      Array(site.data["blog_taxonomy"]).each do |category|
        %w[ko en].each do |lang|
          prefix = lang == "en" ? "en/" : ""
          other_prefix = lang == "en" ? "" : "en/"
          add(site, "#{prefix}blog/category/#{category['id']}", {
            "layout" => "category", "title" => category["title_#{lang}"],
            "description" => category["description_#{lang}"], "lang" => lang,
            "primary_category" => category["id"], "category_data" => category,
            "alternate_url" => "/#{other_prefix}blog/category/#{category['id']}/",
            "alternate_lang" => lang == "en" ? "ko" : "en"
          })
          Array(category["children"]).each do |child|
            add(site, "#{prefix}blog/category/#{category['id']}/#{child['id']}", {
              "layout" => "category", "title" => child["title_#{lang}"],
              "description" => category["description_#{lang}"], "lang" => lang,
              "primary_category" => category["id"], "subcategory" => child["id"],
              "category_data" => category, "child_data" => child,
              "alternate_url" => "/#{other_prefix}blog/category/#{category['id']}/#{child['id']}/",
              "alternate_lang" => lang == "en" ? "ko" : "en"
            })
          end
        end
      end
    end

    def generate_roadmaps(site)
      Array(site.data["blog_roadmaps"]).each do |roadmap|
        add(site, "blog/roadmaps/#{roadmap['id']}", {
          "layout" => "roadmap", "roadmap_id" => roadmap["id"], "lang" => "ko",
          "title" => roadmap["title_ko"], "description" => roadmap["goal_ko"],
          "alternate_url" => "/en/blog/roadmaps/#{roadmap['id']}/", "alternate_lang" => "en"
        })
        add(site, "en/blog/roadmaps/#{roadmap['id']}", {
          "layout" => "roadmap", "roadmap_id" => roadmap["id"], "lang" => "en",
          "title" => roadmap["title_en"], "description" => roadmap["goal_en"],
          "alternate_url" => "/blog/roadmaps/#{roadmap['id']}/", "alternate_lang" => "ko"
        })
      end
    end

    def generate_english_series(site)
      Array(site.data["blog_series"]).each do |series|
        add(site, "en/blog/series/#{series['id']}", {
          "layout" => "series", "series_id" => series["id"], "lang" => "en",
          "title" => series["title_en"], "description" => series["summary_en"],
          "alternate_url" => "/blog/series/#{series['id']}/", "alternate_lang" => "ko"
        })
      end
    end

    def generate_types(site)
      %w[tutorial study-note project-log troubleshooting paper-review].each do |type|
        add(site, "blog/type/#{type}", {
          "layout" => "category", "title" => type.tr("-", " ").split.map(&:capitalize).join(" "),
          "description" => "글 유형별 기술 기록", "lang" => "ko", "post_type" => type
        })
      end
    end
  end
end
