.PHONY: clean
## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Render quarto report
.PHONY: render-quarto

render-quarto:
	@echo "Rendering quarto report"
	@quarto render quarto/$(report).qmd
	@echo "DONE"
## Render and save quarto report (enable vs code quarto extension)
.PHONY: preview-quarto

preview-quarto:
	@echo "Preview quarto report"
	@quarto preview quarto/$(report).qmd --to html --no-browser
	@echo "DONE"