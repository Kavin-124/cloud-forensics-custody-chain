import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_architecture_diagram():
    # Ultra-clear 16:9 canvas with high resolution
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#070D1E')
    ax.set_facecolor('#070D1E')

    # High Contrast Forensic Color Palette
    BOX_BG = '#131F37'
    BORDER_CYAN = '#00E5FF'
    BORDER_GREEN = '#00E676'
    BORDER_RED = '#FF1744'
    BORDER_GOLD = '#FFD600'
    
    TEXT_MAIN = '#FFFFFF'
    TEXT_SUB = '#A7D8DE'
    TEXT_LABEL = '#FFEA00'
    ARROW_COLOR = '#00B0FF'

    def draw_box(x, y, w, h, title, subtitle="", border_color=BORDER_CYAN, box_bg=BOX_BG, title_size=15, sub_size=11):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.18",
            facecolor=box_bg,
            edgecolor=border_color,
            linewidth=2.8,
            zorder=3
        )
        ax.add_patch(rect)
        if subtitle:
            ax.text(x + w/2, y + h*0.65, title, color=TEXT_MAIN, fontsize=title_size, fontweight='heavy', ha='center', va='center', zorder=4)
            ax.text(x + w/2, y + h*0.30, subtitle, color=TEXT_SUB, fontsize=sub_size, fontweight='bold', ha='center', va='center', zorder=4)
        else:
            ax.text(x + w/2, y + h/2, title, color=TEXT_MAIN, fontsize=title_size, fontweight='heavy', ha='center', va='center', zorder=4)

    def draw_arrow(x1, y1, x2, y2, label="", label_y_offset=0.25):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(facecolor=ARROW_COLOR, edgecolor=ARROW_COLOR, width=3.2, headwidth=11, headlength=12, shrink=0.04),
            zorder=2
        )
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            # Add small badge behind label for 100% readability
            ax.text(mx, my + label_y_offset, label, color=TEXT_LABEL, fontsize=10.5, fontweight='heavy', ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.25", facecolor='#070D1E', edgecolor=BORDER_GOLD, linewidth=1.2), zorder=5)

    # 1. USER INGESTION LAYER (Top Left)
    draw_box(0.6, 6.2, 3.8, 1.6, 
             "Forensic Seizure Portal", 
             "• Streamlit Web Ingestion UI\n• Case ID, Badge No & Seizure Tag", 
             BORDER_CYAN, title_size=15, sub_size=11.5)

    # Arrow to Crypto Engine
    draw_arrow(4.4, 7.0, 5.8, 7.0, "Upload Evidence File", label_y_offset=0.35)

    # 2. CRYPTOGRAPHIC CORE ENGINE (Top Center)
    draw_box(5.8, 5.9, 4.6, 2.2, 
             "Cryptographic Core Engine", 
             "1. SHA-256 Binary Digest Computation\n2. Secret HMAC-SHA256 Signatures\n3. Merkle Sequential Chain Linking", 
             BORDER_GOLD, title_size=16, sub_size=11.5)

    # Split Arrows from Engine
    draw_arrow(6.6, 5.9, 3.6, 4.8, "Save Raw Bytes", label_y_offset=0.3)
    draw_arrow(9.6, 5.9, 12.0, 4.8, "Append Block Metadata", label_y_offset=0.3)

    # 3. STORAGE LAYER (Mid Left & Mid Right)
    draw_box(1.0, 3.2, 4.2, 1.6, 
             "Secure Evidence Vault", 
             "• Encrypted Binary Repository\n• Immutable File Storage", 
             BORDER_CYAN, title_size=15, sub_size=11.5)

    draw_box(10.2, 3.2, 4.5, 1.6, 
             "Chain of Custody Ledger", 
             "• Sequential ledger.json Record\n• (Prev_Hash  ⟶  Current_Hash)", 
             BORDER_CYAN, title_size=15, sub_size=11.5)

    # Arrows to Verification Engine
    draw_arrow(3.1, 3.2, 6.2, 2.0, "Runtime Disk Re-Hash", label_y_offset=0.3)
    draw_arrow(12.4, 3.2, 9.8, 2.0, "Stored Block Signatures", label_y_offset=0.3)

    # 4. VERIFICATION / AUDIT ENGINE (Bottom Center)
    draw_box(5.4, 0.8, 5.2, 1.7, 
             "Dual-Engine Forensic Auditor", 
             "Layer 1: Real-time File Integrity Check\nLayer 2: Unbroken Merkle Chain Traversal", 
             BORDER_CYAN, title_size=16, sub_size=11.5)

    # Output Arrows
    draw_arrow(5.4, 1.6, 3.6, 1.6, "Hash Mismatch Found", label_y_offset=0.3)
    draw_arrow(10.6, 1.6, 12.0, 1.6, "Hashes 100% Match", label_y_offset=0.3)

    # 5. OUTPUTS (Bottom Left & Right)
    draw_box(0.5, 0.8, 3.1, 1.6, 
             "🔴 RED ALERT", 
             "TAMPER DETECTED!\nEvidence Altered at Block #N", 
             BORDER_RED, title_size=16, sub_size=11.5)

    draw_box(12.0, 0.8, 3.4, 1.6, 
             "🟢 COURT CERTIFICATE", 
             "Sec 65B Compliant Seal\nAutomated Official PDF", 
             BORDER_GREEN, title_size=15, sub_size=11.5)

    # Main Title Header
    plt.title("CRYPTOGRAPHIC CHAIN OF CUSTODY SYSTEM — ARCHITECTURE DIAGRAM", 
              color=TEXT_MAIN, fontsize=17, fontweight='heavy', pad=25)

    ax.set_xlim(0, 16.0)
    ax.set_ylim(0.2, 8.6)
    ax.axis('off')

    plt.tight_layout()
    output_img = "architecture_diagram.png"
    plt.savefig(output_img, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Architecture diagram re-generated with crystal clear bold fonts: '{output_img}'!")

if __name__ == "__main__":
    draw_architecture_diagram()
