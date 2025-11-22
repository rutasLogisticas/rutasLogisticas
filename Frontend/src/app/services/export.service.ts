import { Injectable } from '@angular/core';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';


@Injectable({
  providedIn: 'root'
})
export class ExportService {
  private buildCSV(headers: string[], rows: (string | number | null | undefined)[][]): string {
    const separator = ';';

    const headerRow = headers
      .map((h) => `"${String(h).replace(/"/g, '""')}"`)
      .join(separator);

    const dataRows = rows.map((row) =>
      row
        .map((cell) => {
          const value = cell === null || cell === undefined ? '' : String(cell);
          return `"${value.replace(/"/g, '""')}"`;
        })
        .join(separator)
    );

    return [headerRow, ...dataRows].join('\r\n');
  }

  private downloadFile(filename: string, mimeType: string, content: string | Blob): void {
    const blob = content instanceof Blob ? content : new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();

    URL.revokeObjectURL(url);
  }

  /** Exportar a CSV (Excel lo abre sin problema) */
  downloadCSV(filename: string, headers: string[], rows: (string | number | null | undefined)[][]): void {
    if (!filename.toLowerCase().endsWith('.csv')) {
      filename += '.csv';
    }
    const csvContent = this.buildCSV(headers, rows);
    this.downloadFile(filename, 'text/csv;charset=utf-8;', csvContent);
  }

  /** Exportar “Excel” (mismo contenido CSV pero con extensión .xlsx para verse más fino) */
  downloadExcel(filename: string, headers: string[], rows: (string | number | null | undefined)[][]): void {
    if (!filename.toLowerCase().endsWith('.xlsx')) {
      filename += '.xlsx';
    }
    const csvContent = this.buildCSV(headers, rows);
    // Excel abre esto sin problema aunque internamente sea CSV
    this.downloadFile(
      filename,
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      csvContent
    );
  }

  /** Exportar a PDF usando jsPDF + autoTable */
  downloadPdf(
    filename: string,
    title: string,
    headers: string[],
    rows: (string | number | null | undefined)[][]
  ): void {
    if (!filename.toLowerCase().endsWith('.pdf')) {
      filename += '.pdf';
    }

    const doc = new jsPDF('l', 'mm', 'a4'); // landscape
    doc.setFontSize(14);
    doc.text(title, 14, 14);

    autoTable(doc, {
      startY: 20,
      head: [headers],
      body: rows.map((r) => r.map((c) => (c === null || c === undefined ? '' : String(c)))),
      styles: { fontSize: 8 },
      headStyles: { fillColor: [41, 128, 185] }
    });

    doc.save(filename);
  }
}
