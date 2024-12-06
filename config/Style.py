

class Style:
    def __init__(self):
        clr_primary = "#B774FE"
        clr_primary_dark = "#006da8"
        clr_primary_light = "#431D69"
        
        clr_secondary = "#42105c"
        clr_secondary_dark = "#7695FF"
        clr_secondary_light = "#96C9F4"
        
        clr_success = "#9681FA"
        clr_success_dark = "#78bb11"
        clr_success_light = "#97df26"
        
        clr_error = "#e9223f"
        clr_error_dark = "#eb1030"
        clr_error_light = "#e6334d"

        clr_white = "#fff"
        clr_light = "#fafafa"
        clr_text = "#585858"

        self._style_ = {
            "side_menu" : """
                QListWidget {{
                    border: none;
                    background-color: {bg};
                    padding: 20px 5px;
                    
                }}

                QListWidget::item {{
                    color: {clr};
                    padding: 5px;
                    border-radius: 5px;
                    outline: none;
                    border: none;
                    text-align: left;
                }}

                QListWidget::item:selected {{
                    background: {bg_selected};
                    color: {clr_selected};
                    outline: none;
                    border: none;
                }}

                QListWidget::item:first {{
                    background-color: #eee;
                    width: 40px;
                    height: 40px;
                }}
            """.format(bg=clr_primary, clr=clr_white, bg_selected=clr_white, clr_selected=clr_primary),

            "main_style" : """
                background: {clr_primary};
            """.format(clr_primary=clr_primary),
            
            "bg_white" : """
                background: {clr_white};
            """.format(clr_white=clr_white),

            "btn-default" : """
                QPushButton {{
                    outline: none;
                    background-color: #fff;
                    color: {clr_text};
                    border: 1px solid {clr_text};
                    letter-spacing: 0.5px;
                    border-radius: 0px;
                }}
            """.format(clr_text=clr_text),
            
            "btn-icon" : """
                QPushButton {{
                    outline: none;
                    background-color: #fff;
                    border: none;
                }}
            """.format(clr_text=clr_text),
            
            "btn-primary" : """
                QPushButton:hover {{
                    background-color: {bg_hv};
                    color: {clr_hv};
                    border-color: {bg_hv};
                }}
                               
                QPushButton:pressed {{
                    background-color: {bg_pd};
                    color: {clr_pd};
                    border-color: {bg_pd};
                }}
            """.format(bg_hv=clr_primary_light, clr_hv=clr_white, bg_pd=clr_primary_dark, clr_pd=clr_white),
            
            "btn-secondary" : """           
                QPushButton:hover {{
                    background-color: {bg_hv};
                    color: {clr_hv};
                    border-color: {bg_hv};
                }}
                               
                QPushButton:pressed {{
                    background-color: {bg_pd};
                    color: {clr_pd};
                    border-color: {bg_pd};
                }}
            """.format(bg_hv=clr_secondary_light, clr_hv=clr_white, bg_pd=clr_secondary_dark, clr_pd=clr_white),
            
            "btn-success" : """           
                QPushButton:hover {{
                    background-color: {bg_hv};
                    color: {clr_hv};
                    border-color: {bg_hv};
                }}
                               
                QPushButton:pressed {{
                    background-color: {bg_pd};
                    color: {clr_pd};
                    border-color: {bg_pd};
                }}
            """.format(bg_hv=clr_success_light, clr_hv=clr_white, bg_pd=clr_success_dark, clr_pd=clr_white),
            
            "btn-error" : """        
                QPushButton:hover {{
                    background-color: {bg_hv};
                    color: {clr_hv};
                    border-color: {bg_hv};
                }}
                               
                QPushButton:pressed {{
                    background-color: {bg_pd};
                    color: {clr_pd};
                    border-color: {bg_pd};
                }}
            """.format(bg_hv=clr_error_light, clr_hv=clr_white, bg_pd=clr_error_dark, clr_pd=clr_white),

            "tab_style" : """
                QTabBar {{
                    border-top: 1px solid #93abc5;
                    padding: 20px 0 0;
                }}

                QTabWidget::pane {{
                    border: none;
                    border: 0;
                    background: {bg_lt};
                }}

                QTabBar::tab {{
                    background: {bg_light};
                    color: {clr_text};
                    padding: 10px;
                    border: none;
                }}

                QTabBar::tab:selected {{
                    background: {bg_select};
                    color: {clr_white}
                }}
            """.format(bg_light=clr_light, bg_lt=clr_success, clr_white=clr_white, clr_text=clr_text, bg_select=clr_secondary),

            "thead" : """
                QHeaderView::section {{
                    background-color: #e0e8f6;
                    color: #000;
                    padding: 5px;
                    border: 1px solid #ccc; 
                    border-left: none;
                }}

                QHeaderView::section:nth-child(1){{
                    border-left: 1px solid #ccc;
                }}
                
            """.format(clr_white=clr_white),

            "tbody": """
                QTableWidget {{
                   border-collapse: collapse; 
                }}
                
                QTableWidget::item:selected {{
                    background-color: {bg};
                }}
            """.format(bg=clr_primary),

            "combobox": """
                QComboBox {{
                    border: 1px solid {bd_clr};
                    color: {clr_text};
                    padding: 1px 5px 1px 20px;
                }}

                QComboBox:editable {{
                    background: {clr_white};
                }}
                
                QComboBox:!editable, QComboBox::drop-down:editable {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 {clr_white}, stop: 0.4 {clr_white},
                                                stop: 0.5 {clr_white}, stop: 1.0 {clr_white});
                }}

                QComboBox:on {{
                    padding: 10px 5px 10px 20px;
                }}

                QComboBox QAbstractItemView {{
                    border: 1px solid {bd_clr};
                    color: {clr_text};
                    selection-background-color: {sel_bg};
                    selection-color: {clr_white};
                    background-color: {bg_items};
                }}
        """.format(clr_text=clr_text, bd_clr=clr_text, sel_bg=clr_primary, clr_white=clr_white, bg_items=clr_white),

        "wizard": """
            QWizard {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }

            QWizard::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                top: -10px;
                font-size: 18px;
                font-weight: bold;
            }

            QWizardPage {
                background-color: {bg};
                border: none;
                padding: 20px;
            }

            QWizard::button {
                border: none;
                border-radius: 0;
                padding: 10px;
                font-size: 14px;
            }

            QWizard::button:hover {
                background-color: red;
            }

            QWizard::button:pressed {
                background-color: blue;
            }

            QWizard::button:checked {
                background-color: green;
            }

            QWizard::button:checked:hover {
                background-color: yellow;
            }

            QWizard::button:checked:pressed {
                background-color: orange;
            }
        """,

        "label_file_name": """
            text-align: center;
        """, 

        "label_scoor": """
            text-align: center;
            color: {clr}
        """.format(clr=clr_text), 

        "progress_bar": """
            QProgressBar {{
                text-align: center;
                color: transparent;
            }}
            QProgressBar::chunk {{
                background-color: {bg};
            }}
        """.format(bg=clr_success)
        }

    def get(self, key):
        return self._style_[key]