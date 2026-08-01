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
      generate_coursework(site)
      generate_engineering_tracks(site)
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
        %w[ko en].each do |lang|
          prefix = lang == "en" ? "en/" : ""
          alternate_prefix = lang == "en" ? "" : "en/"
          data = directory_data(mode, titles[lang == "en" ? 1 : 0], lang)
          data["category_ids"] = category_ids(site, lang) if mode == "categories"
          data["roadmap_ids"] = roadmap_ids(site, lang) if mode == "roadmaps"
          next if mode == "categories" && data["category_ids"].empty?
          next if mode == "roadmaps" && data["roadmap_ids"].empty?

          if directory_available?(site, mode, lang == "en" ? "ko" : "en")
            add_alternate(data, "/#{alternate_prefix}blog/#{mode}/", lang == "en" ? "ko" : "en")
          end
          add(site, "#{prefix}blog/#{mode}", data)
        end
      end
    end

    def directory_data(mode, title, lang)
      {
        "layout" => "blog-directory",
        "mode" => mode,
        "title" => title,
        "description" => title,
        "lang" => lang
      }
    end

    def generate_categories(site)
      Array(site.data["blog_taxonomy"]).each do |category|
        %w[ko en].each do |lang|
          parent_posts = category_posts(site, lang, category["id"])
          track = Array(site.data["engineering_tracks"]).find { |item| item["category_id"] == category["id"] }
          courses = category["id"] == "major-foundations" ? Array(site.data["coursework_courses"]) : []
          next if parent_posts.empty? && !track && courses.empty?

          prefix = lang == "en" ? "en/" : ""
          other_prefix = lang == "en" ? "" : "en/"
          data = {
            "layout" => "category", "title" => category["title_#{lang}"],
            "description" => category["description_#{lang}"], "lang" => lang,
            "primary_category" => category["id"], "category_data" => category,
            "track_data" => track, "coursework_courses" => courses
          }
          add_alternate(data, "/#{other_prefix}blog/category/#{category['id']}/", lang == "en" ? "ko" : "en")
          add(site, "#{prefix}blog/category/#{category['id']}", data)
          Array(category["children"]).each do |child|
            posts = category_posts(site, lang, category["id"], child["id"])
            course = courses.find { |item| item["id"] == child["id"] }
            next if posts.empty? && !course

            child_data = {
              "layout" => "category", "title" => child["title_#{lang}"],
              "description" => child["description_#{lang}"] || category["description_#{lang}"], "lang" => lang,
              "primary_category" => category["id"], "subcategory" => child["id"],
              "category_data" => category, "child_data" => child,
              "course_data" => course
            }
            add_alternate(child_data, "/#{other_prefix}blog/category/#{category['id']}/#{child['id']}/", lang == "en" ? "ko" : "en")
            add(site, "#{prefix}blog/category/#{category['id']}/#{child['id']}", child_data)
          end
        end
      end
    end

    def generate_roadmaps(site)
      Array(site.data["blog_roadmaps"]).each do |roadmap|
        %w[ko en].each do |lang|
          prefix = lang == "en" ? "en/" : ""
          other_prefix = lang == "en" ? "" : "en/"
          data = {
            "layout" => "roadmap", "roadmap_id" => roadmap["id"], "lang" => lang,
            "title" => roadmap["title_#{lang}"], "description" => roadmap["goal_#{lang}"]
          }
          add_alternate(data, "/#{other_prefix}blog/roadmaps/#{roadmap['id']}/", lang == "en" ? "ko" : "en")
          add(site, "#{prefix}blog/roadmaps/#{roadmap['id']}", data)
        end
      end
    end

    def generate_coursework(site)
      Array(site.data["coursework_courses"]).each do |course|
        %w[ko en].each do |lang|
          prefix = lang == "en" ? "en/" : ""
          other_prefix = lang == "en" ? "" : "en/"
          course_dir = "#{prefix}coursework/#{course['id']}"
          data = {
            "layout" => "coursework-course", "lang" => lang,
            "title" => course["title_#{lang}"], "description" => course["summary_#{lang}"],
            "course_data" => course, "image" => course["thumbnail"]
          }
          add_alternate(data, "/#{other_prefix}coursework/#{course['id']}/", lang == "en" ? "ko" : "en")
          add(site, course_dir, data)

          Array(course["units"]).each do |unit|
            unit_slug = format("week-%02d-%s", unit["order"], unit["slug"])
            unit_data = {
              "layout" => "coursework-unit", "lang" => lang,
              "title" => unit["title_#{lang}"],
              "description" => course["summary_#{lang}"],
              "course_data" => course, "unit_data" => unit,
              "image" => course["thumbnail"]
            }
            add_alternate(unit_data, "/#{other_prefix}coursework/#{course['id']}/#{unit_slug}/", lang == "en" ? "ko" : "en")
            add(site, "#{course_dir}/#{unit_slug}", unit_data)
          end
        end
      end
    end

    def generate_engineering_tracks(site)
      Array(site.data["engineering_tracks"]).each do |track|
        %w[ko en].each do |lang|
          prefix = lang == "en" ? "en/" : ""
          other_prefix = lang == "en" ? "" : "en/"
          track_dir = "#{prefix}study/#{track['id']}"
          data = {
            "layout" => "engineering-track", "lang" => lang,
            "title" => track["title_#{lang}"], "description" => track["summary_#{lang}"],
            "track_data" => track, "image" => track["thumbnail"]
          }
          add_alternate(data, "/#{other_prefix}study/#{track['id']}/", lang == "en" ? "ko" : "en")
          add(site, track_dir, data)

          Array(track["units"]).each do |unit|
            unit_data = {
              "layout" => "engineering-unit", "lang" => lang,
              "title" => unit["title_#{lang}"], "description" => unit["body_#{lang}"],
              "track_data" => track, "unit_data" => unit, "image" => unit["image"]
            }
            add_alternate(unit_data, "/#{other_prefix}study/#{track['id']}/#{unit['slug']}/", lang == "en" ? "ko" : "en")
            add(site, "#{track_dir}/#{unit['slug']}", unit_data)
          end
        end
      end
    end

    def generate_english_series(site)
      Array(site.data["blog_series"]).each do |series|
        next if series["hidden"]

        data = {
          "layout" => "series", "series_id" => series["id"], "lang" => "en",
          "title" => series["title_en"], "description" => series["summary_en"]
        }
        add_alternate(data, "/blog/series/#{series['id']}/", "ko")
        add(site, "en/blog/series/#{series['id']}", data)
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

    def localized_posts(site, lang)
      site.posts.docs.select { |post| post.data["lang"] == lang && post.data["draft"] != true }
    end

    def category_posts(site, lang, category_id, child_id = nil)
      localized_posts(site, lang).select do |post|
        post.data["primary_category"] == category_id && (!child_id || post.data["subcategory"] == child_id)
      end
    end

    def series_posts(site, lang, series_id)
      localized_posts(site, lang).select { |post| post.data["series"] == series_id }
    end

    def roadmap_posts(site, roadmap, lang)
      series_ids = Array(roadmap["steps"]).map { |step| step["series"] }.compact.uniq
      localized_posts(site, lang).select { |post| series_ids.include?(post.data["series"]) }
    end

    def category_ids(site, lang)
      ids = localized_posts(site, lang).map { |post| post.data["primary_category"] }.compact
      ids.concat(Array(site.data["engineering_tracks"]).map { |track| track["category_id"] })
      ids << "major-foundations" if Array(site.data["coursework_courses"]).any?
      ids.uniq
    end

    def roadmap_ids(site, lang)
      Array(site.data["blog_roadmaps"]).select { |roadmap| roadmap_posts(site, roadmap, lang).any? }.map { |roadmap| roadmap["id"] }
    end

    def directory_available?(site, mode, lang)
      return category_ids(site, lang).any? if mode == "categories"
      return roadmap_ids(site, lang).any? if mode == "roadmaps"

      localized_posts(site, lang).any?
    end

    def add_alternate(data, url, lang)
      data["alternate_url"] = url
      data["alternate_lang"] = lang
    end

  end
end
