#!/bin/bash
# list-samples.sh - List available sample files

echo "📁 Available Sample Files:"
echo "=========================="
echo ""

# List CSV files
echo "📊 CSV Data Files:"
ls -la samples/*.csv 2>/dev/null | while read line; do
    filename=$(echo "$line" | awk '{print $9}' | sed 's|samples/||')
    size=$(echo "$line" | awk '{print $5}')
    echo "  📄 $filename ($size bytes)"
done

echo ""
echo "🌐 Web Files:"
ls -la samples/*.html 2>/dev/null | while read line; do
    filename=$(echo "$line" | awk '{print $9}' | sed 's|samples/||')
    size=$(echo "$line" | awk '{print $5}')
    echo "  📄 $filename ($size bytes)"
done

echo ""
echo "🚀 Usage Examples:"
echo "  python main.py --file samples/sample.csv --dry-run"
echo "  aws s3 cp samples/sample.csv s3://foreman-dev-csv-uploads/"
echo "" 