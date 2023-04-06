nesta_template = """{% block postamble %}

    <style type="text/css">
      @font-face {
        font-family: "Averta";
        src: url("Intelligent Design - Averta-Regular.otf") format("truetype");
        }
      p.customfont { 
        font-family: "Averta";
        }

    .bk-root .bk-btn-primary  {
        color: #FDFEFE;
        background-color: #0000FF;
        border-color: #21618C;
        }

    .bk-root .bk-btn-default.bk-active {
        color: #FDFEFE;
        background-color: #0000FF;
        border-color: #21618C;
        }

    input[type="checkbox"] {
        accent-color: 
        }
    
    .bk-root {font-family: Averta}

    .bok-root div.bk-tooltip.bk-left

    {
        color: #0000FF;
    }

     .bk-root .bk-tooltip {
        color: #0000FF;
    }

    .center {
     
      display: flex;
      justify-content: center;
      font-family: "Averta";

      }

      </style> 
    {% endblock %} """