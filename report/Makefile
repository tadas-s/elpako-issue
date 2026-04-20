REPORT_MD = REPORT.md
REPORT_PDF = elpako-problema.pdf
PANDOC = pandoc
PDF_ENGINE = weasyprint

.PHONY: all clean

all: $(REPORT_PDF)

$(REPORT_PDF): $(REPORT_MD)
	$(PANDOC) $< -o $@ --pdf-engine=$(PDF_ENGINE)

clean:
	rm -f $(REPORT_PDF)
