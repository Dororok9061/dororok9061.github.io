# frozen_string_literal: true

# Simplex ships compatibility assets for its stock layouts. This site keeps the
# theme's compiled SCSS and WOFF2 fonts, while its accessible custom layouts use
# one small Vanilla JS file and do not need jQuery, Lity, icon sprites, WOFF, or
# TTF fallbacks.
Jekyll::Hooks.register :site, :post_read do |site|
  unused_paths = %w[
    /assets/js/jquery.slim.min.js
    /assets/js/lity.min.css
    /assets/js/lity.min.js
    /assets/js/tools.js
    /assets/img/icons/arrow_left.svg
    /assets/img/icons/arrow_right.svg
    /assets/img/icons/simplex_logo.svg
  ].freeze

  site.static_files.reject! do |file|
    path = file.relative_path.tr("\\", "/")
    unused_paths.include?(path) ||
      (path.start_with?("/assets/fonts/") && %w[.ttf .woff].include?(File.extname(path)))
  end
end
