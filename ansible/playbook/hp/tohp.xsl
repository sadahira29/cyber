<?xml version="1.0" encoding="utf-8" ?>
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="utf-8"/>

  <xsl:template match="/configuration">
    <xsl:text>---&#10;</xsl:text>
    <xsl:apply-templates />
  </xsl:template>
  
  <xsl:template match="system/login/user|system/syslog/user/contents|system/syslog/file|system/syslog/file/contents|system/ntp/server|system/sntp/server">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="interfaces/interface_range|interfaces/interface_range/member|interfaces/interface_range/unit/family/ethernet_switching/vlan/members|interfaces/interface|interfaces/interface/unit/family/ethernet_switching/vlan/members">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="snmp/trap_group/targets|snmp/community">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="routing_options/static/route">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="routing_options/static/route/name" mode="loop">
    <xsl:variable name="addr" select="substring-before(text(),'/')"/>
    <xsl:variable name="mask" select="substring-after(text(),'/')"/>
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*) - 1"/>
    </xsl:call-template>
    <xsl:text>- </xsl:text>
    <xsl:value-of select="concat('addr: &quot;',$addr,'&quot;&#10;')"/>
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*)"/>
    </xsl:call-template>
    <xsl:text>mask: &quot;</xsl:text>
    <xsl:call-template name="maskstr">
      <xsl:with-param name="masksize" select="$mask"/>
    </xsl:call-template>
    <xsl:text>&quot;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="protocols/vstp/vlan_group/group|protocols/vstp/vlan_group/group/vlan|protocols/vstp/vlan_group/group/interface|protocols/vstp/vlan/interface">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="vlans/vlan">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="vlans/vlan/ip_address">
    <xsl:variable name="addr" select="substring-before(.,'/')"/>
    <xsl:variable name="mask" select="substring-after(.,'/')"/>
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*)"/>
    </xsl:call-template>
    <xsl:value-of select="concat('ip_address: &quot;',$addr,'&quot;&#10;')"/>
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*)"/>
    </xsl:call-template>
    <xsl:text>mask: &quot;</xsl:text>
    <xsl:call-template name="maskstr">
      <xsl:with-param name="masksize" select="$mask"/>
    </xsl:call-template>
    <xsl:text>&quot;&#10;</xsl:text>
  </xsl:template>

  <xsl:template name="maskstr">
    <xsl:param name="masksize"/>
    <xsl:choose>
      <xsl:when test="$masksize='0'">
	<xsl:text>0.0.0.0</xsl:text>
      </xsl:when>
      <xsl:when test="$masksize='21'">
	<xsl:text>255.255.248.0</xsl:text>
      </xsl:when>
      <xsl:when test="$masksize='24'">
	<xsl:text>255.255.255.0</xsl:text>
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>255.255.255.0</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="spanning_trees/spanning_tree">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="virtual_chassis/member">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template name="loopnode">
    <xsl:if test="../*[name()=name(current())][1]=current()">
      <xsl:call-template name="indent">
	<xsl:with-param name="num" select="count(ancestor::*)"/>
      </xsl:call-template>
      <xsl:value-of select="concat(name(),':&#10;')"/>
    </xsl:if>
    <xsl:for-each select="*">
      <xsl:choose>
	<xsl:when test="position()=1">
	  <xsl:apply-templates select="." mode="loop"/>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:apply-templates select="."/>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="*">
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*)"/>
    </xsl:call-template>
    <xsl:call-template name="printnode"/>
  </xsl:template>

  <xsl:template match="*" mode="loop">
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*) - 1"/>
    </xsl:call-template>
    <xsl:text>- </xsl:text>
    <xsl:call-template name="printnode"/>
  </xsl:template>

  <xsl:template name="printnode">
    <xsl:choose>
      <xsl:when test="name()='keys'">
	<xsl:value-of select="concat('_keys: &quot;', ./text(),'&quot;&#10;')"/>
      </xsl:when>
      <xsl:when test="count(*)=0 and text()">
	<xsl:value-of select="concat(name(),': &quot;', ./text(),'&quot;&#10;')"/>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="concat(name(),':&#10;')"/>
	<xsl:apply-templates />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="indent">
    <xsl:param name="num"/>
    <xsl:if test="$num &gt; 1">
      <xsl:text>  </xsl:text>
      <xsl:call-template name="indent">
	<xsl:with-param name="num" select="$num - 1"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>
</xsl:transform>
