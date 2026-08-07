# frozen_string_literal: true

module StartHereLayoutOverride
  class Generator < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      site.pages.each do |page|
        next unless page.data["mode"] == "start-here"

        page.data["layout"] = "blog-start-here"
        if page.data["lang"] == "en"
          page.data["title"] = "Engineering Research Portfolio · Start Here"
          page.data["description"] = "Paper-style entry point for Hyeongrok Ryu's research, projects, publications, coursework, technical blog, and source collections."
        else
          page.data["title"] = "Engineering Research Portfolio · Start Here"
          page.data["description"] = "류형록의 연구·프로젝트·논문·전공과제·기술 블로그와 원본 자료를 논문형 흐름으로 연결한 시작 페이지"
        end
        page.data["image"] = "/assets/images/research/start-here-domain-map.svg"
      end
    end
  end
end
