project = "Wi-Fi Analyzer"
author = "ASVA Consulting"
copyright = "2026, ASVA Consulting TFE SL"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_gallery.gen_gallery"]
html_theme = "pydata_sphinx_theme"
html_title = "Wi-Fi Analyzer"
exclude_patterns = ["_build"]
sphinx_gallery_conf = {
    "examples_dirs": "../examples",
    "gallery_dirs": "gallery",
    "filename_pattern": r"/plot_",
    "download_all_examples": False,
    "abort_on_example_error": True,
    "remove_config_comments": True,
}
html_theme_options = {
    "github_url": "https://github.com/julianascencio/wifi-analyzer",
    "show_toc_level": 2,
}
