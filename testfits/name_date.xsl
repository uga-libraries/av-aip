<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet 
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xpath-default-namespace="http://hul.harvard.edu/ois/xml/ns/fits/fits_output"
    exclude-result-prefixes="xs">
    <xsl:output method="text" indent="yes"/>

<xsl:template match="/">
  <xsl:text>filepath,date</xsl:text><xsl:text>&#xa;</xsl:text>
  <xsl:apply-templates select="//fits"/>
</xsl:template>

<xsl:template match="fits">
  <xsl:value-of select="fileinfo/filepath"/><xsl:text>,</xsl:text>
  <xsl:value-of select="fileinfo/fslastmodified"/><xsl:text>,</xsl:text>
  <xsl:text>&#xa;</xsl:text>
</xsl:template>

</xsl:stylesheet>