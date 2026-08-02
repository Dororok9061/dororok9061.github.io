# frozen_string_literal: true

module RFStudyPages
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
      catalog = site.data["rfdh_study_series"] || {}
      articles = Array(catalog["articles"])
      articles.each_with_index do |article, index|
        %w[ko en].each do |lang|
          url = article["url_#{lang}"]
          next unless url

          data = {
            "layout" => "rf-article",
            "lang" => lang,
            "title" => article["title_#{lang}"],
            "description" => article["description_#{lang}"],
            "image" => Array(article["figures"]).first,
            "article_data" => article,
            "rf_previous" => index.positive? ? articles[index - 1] : nil,
            "rf_next" => index + 1 < articles.length ? articles[index + 1] : nil,
            "alternate_url" => article[lang == "en" ? "url_ko" : "url_en"],
            "alternate_lang" => lang == "en" ? "ko" : "en"
          }
          dir = url.sub(%r{^/}, "").sub(%r{/$}, "")
          site.pages << GeneratedPage.new(site, dir, data)
        end
      end

      Array(catalog["series"]).each do |series|
        %w[ko en].each do |lang|
          prefix = lang == "en" ? "/en" : ""
          url = "#{prefix}/blog/series/#{series['id']}/"
          data = {
            "layout" => "rf-series",
            "lang" => lang,
            "title" => series["title_#{lang}"],
            "description" => series["description_#{lang}"],
            "rf_series" => series,
            "alternate_url" => lang == "en" ? url.sub(%r{^/en}, "") : "/en#{url}",
            "alternate_lang" => lang == "en" ? "ko" : "en"
          }
          dir = url.sub(%r{^/}, "").sub(%r{/$}, "")
          site.pages << GeneratedPage.new(site, dir, data)
        end
      end
    end
  end
end
