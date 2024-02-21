<?xml version="1.0" encoding="utf-8" ?>
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="utf-8" indent="yes"/>

  <xsl:template match="/rpc-reply">
    <xsl:apply-templates select="./configuration"/>
  </xsl:template>

  <xsl:template match="protocols/vstp/vlan-group/group/vlan">
    <vlan>
      <name><xsl:value-of select="text()"/></name>
    </vlan>
  </xsl:template>

  <xsl:template match="vlan-group/group/vlan">
    <vlan>
      <name><xsl:value-of select="text()"/></name>
    </vlan>
  </xsl:template>

  <xsl:template match="interfaces/interface-range/unit/family/ethernet-switching/vlan/members|interfaces/interface/unit/family/ethernet-switching/vlan/members">
    <members>
      <name><xsl:value-of select="text()"/></name>
    </members>
  </xsl:template>

  <xsl:template match="*">
    <xsl:element name="{translate(name(), '-.', '__')}">
      <xsl:apply-templates />
    </xsl:element>
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>
</xsl:transform>
